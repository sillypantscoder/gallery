(() => {
	var x = new XMLHttpRequest()
	x.open("GET", "/meta.json")
	x.addEventListener("loadend", () => {
		var meta = JSON.parse(x.responseText)
		for (var i = 0; i < meta.length; i++) {
			var e = document.createElement("div")
			document.querySelector("#grid")?.appendChild(e);
			// Structure
			e.innerHTML = "<div><img></div>"
			// Image
			e.children[0].setAttribute("style", "background-image: url(/thumbnail/" + meta[i].filename + ");")
		}
	})
	x.send()
})();
