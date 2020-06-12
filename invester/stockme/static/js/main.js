$(document).ready(function() {
	//init hide div
	$('#mydiv').hide();

	//Listening form best points input
	document.querySelector('#formSubmit').addEventListener('click', function(e) {
		e.preventDefault();
		makePanel();
	});

	// swap form
	$('#close').click(function() {
		$('#myForm').show();
		$('#mydiv').hide();
	});

	function makePanel() {
		$('#myForm').hide();
		$('#mydiv').show();
		let count = document.getElementById('count').value;
		let timeWindow = document.getElementById('timeWindow').value;
		let short = document.getElementById('short').value;
		let datePanel = localStorage.getItem('datePanel');

		$.ajax({
			url: 'invest',
			type: 'get',
			data: {
				count: count,
				timeWindow: timeWindow,
				short: short,
				datePanel: datePanel
			},
			success: function(result) {
				let today = result.today;
				let dataPoints = result.actual;
				let mydiv = $('#mydiv2');
				let ul = document.createElement('div');

				let ind = 0;
				output = `Best points for ${today}`;
				for (combo of dataPoints) {
					ind++;

					divr = `<div class="input-box">
                            <hr>
                            <p><span class='key'>Buy</span> : ${combo.Buy}</p>
                            <p><span class='key'>Sell</span> : ${combo.Sell}</p>
                            <p><span class='key'>Short</span> : ${combo.Short}</p>
                            <p><span class='key'>Difference</span> : ${combo.Actual_money}</p>
							</div>`;
					if (combo.Short == true) {
						divr = `<div class="input-box">
                            <hr>
                            <p><span class='key'>Sell</span> : ${combo.Sell}</p>
                            <p><span class='key'>Buy</span> : ${combo.Buy}</p>
                            <p><span class='key'>Short</span> : ${combo.Short}</p>
                            <p><span class='key'>Difference</span> : ${combo.Actual_money}</p>
							</div>`;
					}

					output += divr;
				}
				ul.innerHTML = output;
				mydiv.html(output);
			}
		});
	}
	function insertDate(result) {
		myDate = String(result.actDate);

		document.getElementById('dateToday').innerText =
			myDate.slice(0, 4) + '-' + myDate.slice(4, 6) + '-' + myDate.slice(6, 8);
	}
	function main() {
		todayd = localStorage.getItem('datePanel');
		let datePanel = localStorage.getItem('datePanel');
		$.ajax({
			url: 'today',
			data: {
				today: todayd
			},
			success: function(result) {
				let labels = result.labels;
				let data = result.data;
				let predictionData = result.predictionData;
				insertDate(result);
				console.log(`Actual ${result.actDate}\nPredictions ${result.predDatee}`);
				showGraph(labels, data, predictionData);
			}
		});
	}

	function showGraph(labels, data, predictionData) {
		var ctx = document.getElementById('myChart').getContext('2d');
		var chart = new Chart(ctx, {
			// The type of chart we want to create
			type: 'line',

			// The data for our dataset
			data: {
				// labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
				labels: labels,
				datasets: [
					{
						label: 'Actual',
						borderColor: 'rgb(0,255,0)',
						data: data,
						fill: false
					},
					{
						label: 'Prediction',
						borderColor: 'rgb(0,0,255)',
						data: predictionData,
						fill: false
					}
				]
			},

			// Configuration options go here
			options: {
				elements: {
					point: {
						radius: 0
					}
				}
			}
		});
	}

	function complete() {
		console.log('hit1');
		jQuery(function() {
			$('#autocomplete-input').on('keyup', function() {
				var value = $(this).val();

				let x = $.ajax({
					url: 'autoComplete',
					data: {
						search: value
					},
					dataType: 'json',
					success: function(data) {
						list = data.list;
						console.log(Object.keys(list).length);
						var elems = document.querySelector('.autocomplete');
						var instances = M.Autocomplete.init(elems, { data: list, limit: 5, onAutocomplete: init });
						instances.open();
						return 100;
					}
				});
				console.log(x, 'x');
			});
		});
	}
	function init() {
		today = document.getElementById('autocomplete-input').value;
		localStorage.setItem('datePanel', today);
		document.querySelector('.mypage').style.display = 'block';
		main();
		var elems = document.querySelectorAll('.timepicker');
		var instances = M.Timepicker.init(elems, {
			twelveHour: false,
			autoClose: true
		});
	}
	complete();
});
