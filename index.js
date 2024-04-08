(() => {
	var x = new XMLHttpRequest()
	x.open("GET", "/meta.json")
	x.addEventListener("loadend", () => {
		var meta = JSON.parse(x.responseText)
		for (var i = 0; i < meta.length; i++) {
			((info) => {
				var m = document.createElement("div")
				document.querySelector("#grid")?.appendChild(m);
				m.innerHTML = "<div class='card'></div>"
				var e = m.children[0]
				// Structure
				e.innerHTML = "<div class='img-container'><img></div>"
				// Image
				e.children[0].children[0].setAttribute("src", "/thumbnail/" + info.filename)
				e.children[0].children[0].addEventListener("load", () => {
					e.children[0].setAttribute("style", "opacity: 1;")
				})
			})(meta[i]);
		}
	})
	x.send()
})();
