$(document).ready(function(){

    //init hide div
    $('#mydiv').hide()

    //Listening form best points input
    document.querySelector('#formSubmit').addEventListener('click',function(e){
        e.preventDefault()
        makePanel()
    })


    // swap form
    $("#close").click(function(){
        $('#myForm').show()
        $('#mydiv').hide()
    });

    function makePanel(){
        $('#myForm').hide()
        $('#mydiv').show()
        let count = document.getElementById('count').value
        let timeWindow = document.getElementById('timeWindow').value
        let short = document.getElementById('short').value

        $.ajax(
            {url: "invest"
            ,
            type : 'get',
            data:  {
                count:count,
                timeWindow:timeWindow,
                short:short
            },
             success: function(result){
                        let today = result.today
                        let dataPoints = result.actual
                        let mydiv = $("#mydiv2")
                        let ul = document.createElement('div')

                        let ind = 0
                        output = `Best points for ${today}`
                        for (combo of dataPoints){
                            ind++
                            output+=`<div class="input-box">
                            <hr>
                            <p>${combo.Buy}</p>
                            <p>${combo.Sell}</p>
                            <p>${combo.Short}</p>
                            <p>${combo.Actual_money}</p>
                            </div>`
                        }
                        ul.innerHTML  = output
                        mydiv.html(output)
                        

                    }
            }
            );
          }

    $.ajax(
        {url: "today"
        , success: function(result){
                    let labels = result.labels
                    let data = result.data
                    let predictionData = result.predictionData
                    showGraph(labels,data,predictionData)

                }
        }
        );


    function showGraph(labels,data,predictionData){
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                // labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                labels: labels,
                datasets: [{
                    label: 'My First dataset',
                    borderColor: 'rgb(255,0,0)',
                    data: data,
                    fill: false
                },
                {
                    label: 'My second dataset',
                    borderColor: 'rgb(0,255,0)',
                    data: predictionData,
                    fill: false
                }]
            },

            // Configuration options go here
            options: {
                elements:{
                    point:{
                        radius : 0
                    }
                }
            }
        });

    }
});
