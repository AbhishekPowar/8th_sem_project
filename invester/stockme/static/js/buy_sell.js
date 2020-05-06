$(document).ready(function(){
    let i = 1;
    $('#add').click(function(){
        i+=1
        template = `<div class="pair">
                        <div class="input-box col m6">
                            <label for="">Buy${i}</label>
                            <input type="text" name="" id="buy${i}" value="9:30">
                        </div>
                        <div class="input-box col m6">
                            <label for="">Sell${i}</label>
                            <input type="text" name="" id="sell${i}" value="3:30">
                        </div>
                    </div>`
        let div = document.createElement('div')
        div.innerHTML = template
        div.className = 'pair'
        document.getElementById('buySell').appendChild(div)



    })

    $('#calculate').click(function(){

        let out =  document.getElementById('output')
        out.innerHTML = ''
        out.innerText = ''
        for(let p = 1;p<=i;p++){
            let buy = $(`#buy${p}`).val()
            let sell = $(`#sell${p}`).val()
            let ans = document.createElement('div')
            ans.innerText= buy +"  "+sell
            out.appendChild(ans)

        }

    })

});