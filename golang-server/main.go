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
var bandera =0
var bandera2 = 0
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
    if bandera==0{
        err = client.Set("0",data["Porcentaje"],0).Err()
        err = client.Set("1",data["Porcentaje"],0).Err()
        val, err := client.Get("0").Result()
        if err != nil {
            fmt.Println(err)
        }
        fmt.Println("el valor obtenido es : ",val)
        bandera = 1
    }else
    {
        val, err := client.Get("0").Result()
        err = client.Set("0",data["Porcentaje"],0).Err()
        err = client.Set("1",val,0).Err()
        val2, err := client.Get("0").Result()
        if err != nil {
            fmt.Println(err)
        }
        fmt.Println("el valor obtenido es : ",val2)
    }
    client1 := redis.NewClient(&redis.Options{
        Addr: "redis:6379",
        Password: "",
        DB: 1,
    })
    respo, erro := http.Get("http://34.73.214.43/datoscpu")
    if erro != nil {
        log.Fatalln(erro)
    }
    defer respo.Body.Close()
    bodyByteso, _ := ioutil.ReadAll(respo.Body)
    bodyStringo := string(bodyByteso)
    var datao map[string]interface{}
    err1o := json.Unmarshal([]byte(bodyStringo), &datao)
    if err1o != nil {
        panic(err1o)
    }
    if bandera2==0{
        _  = client1.Set("0",datao["Porcentaje"],0).Err()
        _  = client1.Set("1",datao["Porcentaje"],0).Err()
        bandera2 = 1
    }else
    {
        val1, _ := client1.Get("0").Result()
        _  = client1.Set("0",datao["Porcentaje"],0).Err()
        _  = client1.Set("1",val1,0).Err()
    }
}
var router = mux.NewRouter()

func main() {
    router.HandleFunc("/datos", insertardato).Methods("POST")
    http.HandleFunc("/mem",mem)
    http.Handle("/", router)
	fmt.Println("Servidor corriendo en http://localhost:8081/")
	http.ListenAndServe(":80", nil)
}
