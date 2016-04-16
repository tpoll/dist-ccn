package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"sync"
)

const (
	debugFlag   = "-v"
	debugLevel  = "trace"
	lCacheFlag  = "-d"
	lCachePath  = "/home/todd/dist-ccn/test/ndntlv"
	redisIpFlag = "-z"
)

type ProcInfo struct {
	Id         string `json:"id"`
	proc       *exec.Cmd
	Debug      bool   `json:"debug"`
	Dist       bool   `json:"dist"`
	LocalCache bool   `json:"local_cache"`
	RedisIp    string `json:"redis_ip"`
}

type SafeMap struct {
	m map[string]*ProcInfo
	sync.RWMutex
}

var (
	Warning *log.Logger
	Error   *log.Logger
)

func Init(warningHandle io.Writer, errorHandle io.Writer) {
	Warning = log.New(warningHandle,
		"WARNING: ",
		log.Ldate|log.Ltime|log.Lshortfile)

	Error = log.New(errorHandle,
		"ERROR: ",
		log.Ldate|log.Ltime|log.Lshortfile)
}

func main() {
	Init(os.Stdout, os.Stderr)
	nodes := SafeMap{m: make(map[string]*ProcInfo)}
	active := true

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		heartbeat(w, r, &active)
	})
	http.HandleFunc("/start", func(w http.ResponseWriter, r *http.Request) {
		startCCN(w, r, &nodes, &active)
	})
	http.HandleFunc("/stop", func(w http.ResponseWriter, r *http.Request) {
		stopCCN(w, r, &nodes, &active)
	})

	http.ListenAndServe(":8000", nil)
}

func heartbeat(w http.ResponseWriter, r *http.Request, active *bool) {
	if !*active {
		w.WriteHeader(500)
	}
}

func stopCCN(w http.ResponseWriter, r *http.Request, nodes *SafeMap, active *bool) {
	Warning.Println("stopping ccn node")
	if r.Method == "POST" {
		tempStruct := new(ProcInfo)
		response, _ := ioutil.ReadAll(r.Body)
		json.Unmarshal(response, &tempStruct)
		*active = false
		nodes.Lock()
		nodes.m[tempStruct.Id].proc.Process.Kill()
		nodes.m[tempStruct.Id].proc.Process.Wait()
		delete(nodes.m, tempStruct.Id)
		nodes.Unlock()
	}
}

// Starts up the ccn process with heartbeat
func startCCN(w http.ResponseWriter, r *http.Request, nodes *SafeMap, active *bool) {
	Warning.Println("starting ccn node")
	if r.Method == "POST" {
		tempStruct := new(ProcInfo)
		response, _ := ioutil.ReadAll(r.Body)
		json.Unmarshal(response, &tempStruct)
		nodes.Lock()
		if pid, ok := nodes.m[tempStruct.Id]; ok {
			Warning.Printf("ccn-relay  on %s is already running", pid.Id)
		} else {
			fmt.Println(tempStruct)
			fmt.Println(tempStruct.Id)
			proc, err := runCommand(tempStruct)
			if err == nil {
				tempStruct.proc = proc
				nodes.m[tempStruct.Id] = tempStruct
				*active = true
			} else {
				Error.Printf("ERROR: command for %s failed with code %s\n", tempStruct.Id, err)
			}
		}
		nodes.Unlock()
	}
}

func runCommand(data *ProcInfo) (*exec.Cmd, error) {
	version := "ccn-lite"

	args := []string{"-s", "ndn2013", "-u", "9980", "-x", "/tmp/mgmt-relay-a.sock"}

	if data.Dist {
		version = "dist-ccn"
		args = append(args, redisIpFlag)
		args = append(args, data.RedisIp)

	}

	if data.Debug {
		args = append(args, debugFlag)
		args = append(args, debugLevel)
	}

	if data.LocalCache {
		fmt.Println("lcache variablessd")
		args = append(args, lCacheFlag)
		args = append(args, lCachePath)
	}

	outfile, err := os.Create("ccnRelaylog.txt")
	if err != nil {
		panic(err)
	}

	fmt.Println("about to call command")
	os.Setenv("CCNL_HOME", "/home/todd/dist-ccn")
	cmd := exec.Command(fmt.Sprintf("/home/todd/%s/bin/ccn-lite-relay", version), args...)
	cmd.Stdout = outfile
	cmd.Stderr = outfile
	fmt.Println(cmd.Args)
	err = cmd.Start()
	if err != nil {
		return nil, err
	} else {
		return cmd, nil
	}
}