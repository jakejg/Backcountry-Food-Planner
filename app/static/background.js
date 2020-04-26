
if (location.href === `${location.protocol}//${location.host}/`) {
    document.body.style.backgroundImage = "url('/static/images/baker-sunset.jpg')"
}
if (location.href.includes("select-meals")) {
    document.body.style.backgroundImage = "url('/static/images/labyrinth.jpg')"
}

if (location.href.includes("meal-plan")) {
    document.body.style.backgroundImage = "url('/static/images/harding.jpg')"
}

if (location.href.includes("/meals")) {
    document.body.style.backgroundImage = "url('/static/images/ocean-sunset.jpg')"
}

if (location.href.includes("register")) {
    document.body.style.backgroundImage = "url('/static/images/neocola.jpg')"
}
if (location.href.includes("login")) {
    document.body.style.backgroundImage = "url('/static/images/long.jpg')"
}

if (location.href.includes("users")) {
    document.body.style.backgroundImage = "url('/static/images/rocky.jpg')"
}