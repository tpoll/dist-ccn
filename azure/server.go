/* Light wieght server that handles starting and stopping
   ccn nodes on remote machines.
*/

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

type FaceInfo struct {
	TargetIp string `json:"target_ip"`
	Prefix   string `json:"prefix"`
}

type SafeMap struct {
	m map[string]*ProcInfo
	sync.RWMutex
}

var (
	Info  *log.Logger
	Error *log.Logger
)

func Init(InfoHandle io.Writer, errorHandle io.Writer) {
	Info = log.New(InfoHandle,
		"Info: ",
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
	http.HandleFunc("/face", addFace)

	http.ListenAndServe(":8000", nil)
}

func heartbeat(w http.ResponseWriter, r *http.Request, active *bool) {
	if !*active {
		w.WriteHeader(500)
	}
}

func stopCCN(w http.ResponseWriter, r *http.Request, nodes *SafeMap, active *bool) {
	Info.Println("stopping ccn node")
	if r.Method == "POST" {
		tempStruct := new(ProcInfo)
		response, _ := ioutil.ReadAll(r.Body)
		json.Unmarshal(response, &tempStruct)
		*active = false
		if _, ok := nodes.m[tempStruct.Id]; ok {
			nodes.Lock()
			pid := nodes.m[tempStruct.Id].proc.Process.Pid
			Info.Println(pid)
			cmd := exec.Command("sudo", "killall", "ccn-lite-relay")
			err := cmd.Start()
			if err != nil {
				Error.Println(err)
			}
			delete(nodes.m, tempStruct.Id)
			nodes.Unlock()
		} else {
			w.WriteHeader(404)
			Info.Printf("no node to stop")
		}
	}
}

// Starts up the ccn process with heartbeat
func startCCN(w http.ResponseWriter, r *http.Request, nodes *SafeMap, active *bool) {
	Info.Println("starting ccn node")
	if r.Method == "POST" {
		tempStruct := new(ProcInfo)
		response, _ := ioutil.ReadAll(r.Body)
		json.Unmarshal(response, &tempStruct)
		nodes.Lock()
		if pid, ok := nodes.m[tempStruct.Id]; ok {
			Info.Printf("ccn-relay  on %s is already running", pid.Id)
		} else {
			fmt.Println(tempStruct)
			fmt.Println(tempStruct.Id)
			proc, err := runCommand(tempStruct)
			if err == nil {
				tempStruct.proc = proc
				nodes.m[tempStruct.Id] = tempStruct
				*active = true
			} else {
				w.WriteHeader(500)
				Error.Printf("ERROR: command for %s failed with code %s\n", tempStruct.Id, err)
			}
		}
		nodes.Unlock()
	}
}

func runCommand(data *ProcInfo) (*exec.Cmd, error) {
	version := "ccn-lite"
	if data.Dist {
		version = "dist-ccn"
	}

	args := []string{"--preserve-env", fmt.Sprintf("/home/todd/%s/bin/ccn-lite-relay", version), "-s", "ndn2013", "-u", "9980", "-x", "/tmp/mgmt-relay-a.sock"}

	if data.Dist {
		args = append(args, redisIpFlag)
		args = append(args, data.RedisIp)

	}

	if data.Debug {
		args = append(args, debugFlag)
		args = append(args, debugLevel)
	}

	if data.LocalCache {
		args = append(args, lCacheFlag)
		args = append(args, lCachePath)
	}

	outfile, err := os.Create("ccnRelaylog.txt")
	if err != nil {
		panic(err)
	}

	fmt.Println("about to call command")
	os.Setenv("CCNL_HOME", "/home/todd/dist-ccn")
	cmd := exec.Command("sudo", args...)
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

func addFace(w http.ResponseWriter, r *http.Request) {
	Info.Println("Adding Face")
	if r.Method == "POST" {
		tempStruct := new(FaceInfo)
		response, _ := ioutil.ReadAll(r.Body)
		json.Unmarshal(response, &tempStruct)
		Info.Println(tempStruct)
		os.Setenv("CCNL_HOME", "/home/todd/dist-ccn")
		cmd := exec.Command("sudo", "sh", "/home/todd/add_face.sh", tempStruct.TargetIp, tempStruct.Prefix)
		out, err := cmd.Output()
		if err != nil {
			w.WriteHeader(500)
			Error.Printf("Error, no face created %s", err)
		} else {
			Info.Println(out)
		}
	}
}
