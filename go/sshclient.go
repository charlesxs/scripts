package main

import (
	"fmt"
	"golang.org/x/crypto/ssh"
	"io/ioutil"
	"time"
	"net"
	"os"
	"strings"
	"io"
	"strconv"
	"log"
	"sync"
)


type SSH struct {
	Host, User, Password string
	Port int
}


func NewSSH(host, user, password string, port int) *SSH {
	return &SSH{
		Host: host,
		User: user,
		Password: password,
		Port: port,
	}
}


func (s *SSH) Connect() (*ssh.Session, error) {
	config := &ssh.ClientConfig{
		User: s.User,
		Auth: []ssh.AuthMethod{
			ssh.Password(s.Password),
		},
		Timeout: time.Second * 10,
		HostKeyCallback: func(hostname string, remote net.Addr, key ssh.PublicKey) error {
			return nil
		},
	}

	addr := fmt.Sprintf("%s:%d", s.Host, s.Port)
	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		return nil, err
	}

	return client.NewSession()
}


func (s *SSH) Run(cmd string) (stdout, stderr io.Reader, err error) {
	session, err := s.Connect()
	if err != nil {
		return nil, nil, err
	}
	defer session.Close()

	stdout, _ = session.StdoutPipe()
	stderr, _ = session.StderrPipe()

	err = session.Run(cmd)
	return stdout, stderr, err
}


func (s *SSH) PrintRun(cmd string) {
	var res []byte

	// initial session
	session, err := s.Connect()
	if err != nil {
		log.Println(err)
		return
	}
	defer session.Close()

	// set stdout, stderr
	stdout, _ := session.StdoutPipe()
	stderr, _ := session.StderrPipe()

	// run command
	err = session.Run(cmd)
	if err != nil {
		res, _ = ioutil.ReadAll(stderr)
		log.Printf("%s execute failed ~> \n\033[31m%s\033[0m", s.Host, string(res))
		return
	}
	res, _ = ioutil.ReadAll(stdout)
	log.Printf("%s execute ok ~> \n\033[32m%s\033[0m", s.Host, string(res))
}


func main() {
	if len(os.Args) <= 1 {
		fmt.Println("Usage: ", os.Args[0], "command")
		return
	}

	var wg sync.WaitGroup
	cmd := strings.Join(os.Args[1:], " ")
	prefix := "192.168.119."

	for i := 96; i <= 102; i++ {
		wg.Add(1)
		host := prefix + strconv.Itoa(i)
		go func() {
			ssh := NewSSH(host, "user",
						 "pass", 22)
			ssh.PrintRun(cmd)
			wg.Done()
		}()
	}
	wg.Wait()
}
