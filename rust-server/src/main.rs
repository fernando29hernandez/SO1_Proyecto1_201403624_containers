#![feature(proc_macro_hygiene)]

#[macro_use] extern crate rocket;
#[macro_use] extern crate serde_derive;

#[cfg(test)] mod tests;

use std::collections::HashMap;

use rocket::Request;
use rocket::response::Redirect;
use rocket_contrib::templates::Template;
extern crate redis;
use redis::Commands;
#[derive(Serialize)]
struct TemplateContext {
    name: String,
    items: Vec<&'static str>
}
struct envio
{
    indice : String,
    dato : String

}
#[get("/")]
fn index() -> Redirect {
    Redirect::to(uri!(get: name = "Unknown"))
}

#[get("/hello/<name>")]
fn get(name: String) -> Template {
    let context = TemplateContext { name, items: vec!["One", "Two", "Three"] };
    Template::render("index", &context)
}
#[get("/insertar/<indice>/<dato>")]
fn insertar(indice: String,dato: String)->String{
    //let context = TemplateContext { name, items: vec!["One", "Two", "Three"] };
    //Template::render("index", &context)
    let envio_datos = envio{indice,dato};
    let client = redis::Client::open("redis://redis:6379/1").unwrap();

    // set key = “Hello World”
    let _: () = client.set(envio_datos.indice,envio_datos.dato).unwrap();

    // get key
    let key : String = client.get(envio_datos.indice).unwrap();

    println!("key: {}", key);

}

#[catch(404)]
fn not_found(req: &Request<'_>) -> Template {
    let mut map = HashMap::new();
    map.insert("path", req.uri().path());
    Template::render("error/404", &map)
}

fn rocket() -> rocket::Rocket {
    rocket::ignite()
        .mount("/", routes![index, get,insertar])
        .attach(Template::fairing())
        .register(catchers![not_found])
}

fn main() {
    rocket().launch();
}
