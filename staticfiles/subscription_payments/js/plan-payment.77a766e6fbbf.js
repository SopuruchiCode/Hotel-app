const subSelect = document.querySelector('#id_subscription');
const priceElem = document.querySelector('#id_price');
const durationElem = document.querySelector('#id_duration');
const nairaFormat = new Intl.NumberFormat("en-US",{
    style : "currency",
    currency : "NGN",
});
// nairaFormat.formatTo

function removePrevOpaqueImg(){
    let prevOpaqueImg = document.querySelector('.opacity-control');
    if (prevOpaqueImg){
        prevOpaqueImg.classList.remove('opacity-control');
    }
    
};

function makeImgOpaque(id){
    if (id) {
        let img = document.querySelector(`#plan-${id}`);
        img.classList.add('opacity-control');
    }
};

function getCSRFToken(){
    return document.getElementsByName('csrfmiddlewaretoken')[0].value;
};
async function getPlanPrices(){
    try{
        let response = await fetch('/sub-plan-payments/get-plan-prices/',{
            method: 'post',
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
        });
        let pricesData = await response.json();
        subSelect.addEventListener('change', (event) => {
            let value = event.target.value;
            removePrevOpaqueImg();
            if (value) {
                let price = pricesData[value];
                let duration = Math.floor(durationElem.value);
                priceElem.value = nairaFormat.format(price * duration);
                makeImgOpaque(value);  
            }else{
                priceElem.value = nairaFormat.format(0)
            };

        });
        durationElem.addEventListener('change', (event) => {
            let subplan = subSelect.value;
            if (subplan){
                let price = pricesData[subplan];
                let duration = Math.floor(durationElem.value);
                priceElem.value = nairaFormat.format(price * duration);
                durationElem.value = duration;
            } else{
                priceElem.value = nairaFormat.format(0);
            };            
        })
        if (subSelect.value) {                  // To set initial values+
            let subplan = subSelect.value;
            let price = pricesData[subplan];
            let duration = Math.floor(durationElem.value);
            priceElem.value = nairaFormat.format(price * duration);
            durationElem.value = duration;
        }
        
    }
    catch (err) {
        console.log(err)
    }
};

getPlanPrices();