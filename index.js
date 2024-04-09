(() => {
	var x = new XMLHttpRequest()
	x.open("GET", "/meta.json")
	x.addEventListener("loadend", () => {
		/** @type {{ filename: string, date: string, name: string }[]} */
		var meta = JSON.parse(x.responseText)
		for (var i = 0; i < meta.length; i++) {
			((info) => {
				var m = document.createElement("div")
				document.querySelector("#grid")?.appendChild(m);
				m.innerHTML = `<a class='card' href='image/${info.filename}/'></a>`
				var e = m.children[0]
				// Structure
				e.innerHTML = "<div class='img-container'><img></div><div class='hover-info'></div>"
				// Image
				e.children[0].children[0].setAttribute("src", "/image/" + info.filename + "/thumbnail.png")
				e.children[0].children[0].addEventListener("load", () => {
					e.children[0].setAttribute("style", "opacity: 1;")
				})
				// Hover info
				e.children[1].innerHTML = info.name
			})(meta[i]);
		}
	})
	x.send()
})();
