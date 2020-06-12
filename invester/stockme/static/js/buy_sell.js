$(document).ready(function() {
	let i = 1;
	$('#add').click(function() {
		i += 1;
		template = `<div class="pair">
                        <div class="input-box col m6">
                            <label for="">Buy${i}</label>
                            <input type="text" name="" id="buy${i}" class='timepicker' value="09:30">
                        </div>
                        <div class="input-box col m6">
                            <label for="">Sell${i}</label>
                            <input type="text" name="" id="sell${i}" class='timepicker' value="15:30">
						</div>
						
                    </div>`;
		let div = document.createElement('div');
		div.innerHTML = template;
		div.className = 'pair';
		document.getElementById('buySell').appendChild(div);

		var elems = document.querySelectorAll('.timepicker');
		var instances = M.Timepicker.init(elems, {
			twelveHour: false,
			autoClose: true
		});
	});

	$('#calculate').click(async function() {
		let out = document.getElementById('output');

		out.innerText = '';
		out.innerHTML = `<div height='60px'></div>`;
		for (let p = 1; p <= i; p++) {
			let buy = $(`#buy${p}`).val();
			let sell = $(`#sell${p}`).val();
			let today = localStorage.getItem('datePanel');

			// let sell = $(`#sell${p}`).val();
			let ans = document.createElement('div');
			// var response = await fetch(`127.0.0.1:8000/money?start=${buy}&end=${sell}&today=${today}`);
			var response = await fetch(`money?start=${buy}&end=${sell}&today=${today}`);
			var data = await response.json();
			ans.innerText = data.profit;
			term = 'Profit';
			classname = 'green-text';

			if (data.profit < 0) {
				term = 'Loss';
				classname = 'red-text';
			}
			ans.innerHTML = `<div class='PL'>
					<span class="key">${term}</span>
					<span class="key ${classname}">${data.profit}</span>
					</div>`;
			out.appendChild(ans);
		}
	});
});
