use rocket_contrib::templates::Template;

#[get("/")]
fn index() -> Template {
    let context = 0/* object-like value */;
    Template::render("index", &context)
}
fn main() {
    rocket::ignite()
        .mount("/", routes![/* .. */])
        .attach(Template::fairing());
}

