$(document).ready(function() {
	//init hide div
	$('#mydiv').hide();
	var cname = localStorage.getItem('cname').toLowerCase();
	document.querySelector('#head').innerText = cname.toUpperCase();
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
		let dfName = document.querySelector('input[type=radio]:checked').value;

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
				datePanel: datePanel,
				dfName: dfName,
				cname: cname
			},
			success: function(result) {
				let today = result.today;
				let dataPoints = result.actual;
				let mydiv = $('#mydiv2');
				let ul = document.createElement('div');
				let myDate = localStorage.getItem('datePanel');
				let todayDate = myDate.slice(0, 4) + '-' + myDate.slice(4, 6) + '-' + myDate.slice(6, 8);
				document.querySelector('#dateme').innerText = todayDate;
				let ind = 0;
				term = dfName[0].toUpperCase() + dfName.slice(1, dfName.length);
				output = `${term} data   <span class='right'>${todayDate}</span>`;
				for (combo of dataPoints) {
					ind++;
					clr = 'green-text';
					if (combo.Actual_money < 0) {
						clr = 'red-text';
					}
					divr = `<div class="input-box buySellid">
                            <hr>
                            <p><span class='key space'>Buy</span> <span class='valbs'>${combo.Buy}<span> </p>
                            <p><span class='key space'>Sell</span>  <span class='valbs'>${combo.Sell}<span> </p>
                            <p><span class='key space'>Short</span>  <span class='valbs'>${combo.Short}<span> </p>
                            <p><span class='key space '>Difference</span>  <span class='valbs ${clr}'>${combo.Actual_money}<span> </p>
							</div>`;
					if (combo.Short == true) {
						divr = `<div class="input-box buySellid">
                            <hr>
                            <p><span class='key space'>Sell</span>  <span class='valbs'>${combo.Sell}<span> </p>
                            <p><span class='key space'>Buy</span> <span class='valbs'>${combo.Buy}<span> </p>
                            <p><span class='key space'>Short</span>  <span class='valbs'>${combo.Short}<span> </p>
                            <p><span class='key space' >Difference</span>  <span class='valbs ${clr}'>${combo.Actual_money}<span> </p>
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
				today: todayd,
				cname: cname
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
						fill: false,
						hidden: false
					},
					{
						label: 'Prediction',
						borderColor: 'rgb(0,0,255)',
						data: predictionData,
						fill: false,
						hidden: true
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
						search: value,
						cname: cname
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
		makePanel();
	}
	complete();
});
