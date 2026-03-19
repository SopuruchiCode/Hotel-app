const yesBtn = document.querySelector('.yes');
const noBtn = document.querySelector('.no');
// const form = document.getElementById('form-set');


const option = {
    'yes' : 'yes',
    'no' : 'no'
}
const buttons = [yesBtn, noBtn];
function getCSRFToken(){
    return document.getElementsByName('csrfmiddlewaretoken')[0].value;
}
// form.addEventListener('submit', (event) => {
//     event.preventDefault();
// })


yesBtn.addEventListener('click', async () => {
    try{
        let response = await fetch('/sub-plan-payments/payment-confirmation/', {
            method: 'post',
            headers: {
                // 'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
                'perms': 'transaction-processing'
            },
            body: JSON.stringify({'permission': option[yesBtn.id]})
        })
        let content_type = response.headers.get('content-type');
        if (content_type && content_type == 'application/json') {
            let data = await response.json();
            location.replace(data['new_url'])
        }
        else{
            let data = await response.text()
            document.querySelector('body').innerHTML = data;
        }
        
    }catch (err){
        console.log(err)
    };
});

noBtn.addEventListener('click', async () => {
    try{
        let response = await fetch('/sub-plan-payments/payment-confirmation/', {
            method: 'post',
            headers: {
                // 'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
                'perms': 'transaction-processing'
            },
            body: JSON.stringify({'permission': option[noBtn.id]})
        });
        let data = await response.json();
        location.replace(data['new_url'])
    }catch (err){
        console.log(err)
    };
})
