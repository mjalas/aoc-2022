package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	f, err := os.Open("input.txt")
    if err != nil {
        log.Fatal(err)
    }
    // remember to close the file at the end of the program
    defer f.Close()

    // read the file line by line using scanner
    scanner := bufio.NewScanner(f)
	var l := []string{}
    for scanner.Scan() {
        // do something with a line
		var line = scanner.Text()
		if line == "" {
			fmt.Println("switch")
		} else {
			fmt.Println(line)
			
		}
		// line := scanner.Text()
		// if line == "" {
		// 	sum := 0
		// 	for e := l.Front(); e != nil; e = e.Next() {
		// 		sum := sum + e
		// 		fmt.Println(e)
		// 	}
		// } else {
		// 	calories, err := strconv.Atoi(line)
		// 	if err != nil {
		// 		// ... handle error
		// 		panic(err)
		// 	}
		// 	l.PushBack(calories)
	}
        // fmt.Printf("line: %s\n", scanner.Text())
}

    // if err := scanner.Err(); err != nil {
    //     log.Fatal(err)
    // }
 