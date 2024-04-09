var filename = location.pathname.split("/")[2];
(() => {
	var x = new XMLHttpRequest()
	x.open("GET", "/meta.json")
	x.addEventListener("loadend", () => {
		/** @type {{ filename: string, date: string, name: string }[]} */
		var meta = JSON.parse(x.responseText)
		for (var i = 0; i < meta.length; i++) {
			if (meta[i].filename == filename) {
				// yay
				var title = document.querySelector("#title")
				if (title instanceof HTMLElement) title.innerText = meta[i].name
				var date = document.querySelector("#date")
				if (date instanceof HTMLElement) date.innerText = meta[i].date
			}
		}
	})
	x.send()
})();
