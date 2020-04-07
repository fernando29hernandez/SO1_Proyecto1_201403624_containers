package main

import (
	"fmt"
	"net/http"
    "github.com/gorilla/mux"
	"github.com/go-redis/redis"
    "time"
    "encoding/json"
    "io/ioutil"
    "log"
)
type test_struct struct {
	Test string
}
type Todo struct {
	total   string    `json:"Total"`
	consumida     string    `json:"Consumida"`
	porcentaje     string `json:"Porcentaje"`
}	
func mem(response http.ResponseWriter, request *http.Request) {

	http.ServeFile(response, request, "memoria.html")
}
var myClient = &http.Client{Timeout: 10 * time.Second}
func getJson(url string, target interface{}) error {
    r, err := myClient.Get(url)
    if err != nil {
        return err
    }
    defer r.Body.Close()

    return json.NewDecoder(r.Body).Decode(target)
}
func insertardato(w http.ResponseWriter, r *http.Request){
    client := redis.NewClient(&redis.Options{
        Addr: "redis:6379",
        Password: "",
        DB: 0,
    })
    resp, err := http.Get("http://34.73.214.43/datosmemoria")
    if err != nil {
        log.Fatalln(err)
    }
    defer resp.Body.Close()
    bodyBytes, _ := ioutil.ReadAll(resp.Body)

    // Convert response body to string
    bodyString := string(bodyBytes)
    fmt.Println("API Response as String:\n" + bodyString)

    // Convert response body to Todo struct
    var todoStruct Todo
    json.Unmarshal(bodyBytes, &todoStruct)
	t := time.Now()
	fecha := fmt.Sprintf("%d-%02d-%02dT%02d:%02d:%02d",
		t.Year(), t.Month(), t.Day(),
		t.Hour(), t.Minute(), t.Second())

	fmt.Println("La fecha actual es =>", fecha)
    var data map[string]interface{}
    err1 := json.Unmarshal([]byte(bodyString), &data)
    if err1 != nil {
        panic(err1)
    }
    fmt.Println(data["Porcentaje"])
    err = client.Set(fecha,data["Porcentaje"], 0).Err()
    val, err := client.Get(fecha).Result()
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println("el valor obtenido es : ",val)
}
var router = mux.NewRouter()

func main() {
    router.HandleFunc("/datos", insertardato).Methods("POST")
    http.HandleFunc("/mem",mem)
    http.Handle("/", router)
	fmt.Println("Servidor corriendo en http://localhost:8081/")
	http.ListenAndServe(":80", nil)
}
