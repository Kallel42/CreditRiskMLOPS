var MS;
var HO;
var CO;
var income;
var age;
var experience;
var state;
var currYears;

var loader = document.getElementsByClassName('loader');

function MSValue() {
    var ele = document.getElementsByName('M');
      
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked)
        MS=ele[i].value;
    }
    return MS
}
function HOValue() {
    var ele = document.getElementsByName('HO');
      
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked)
        HO=ele[i].value;
    }
    return HO
}
function COValue() {
    var ele = document.getElementsByName('co');
      
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked)
        CO=ele[i].value;
    }
    return CO
}

var SUB=document.getElementById("Sub");
var risk_0=document.getElementById("risk_0");
var risk_1=document.getElementById("risk_1");

document.getElementById("income").addEventListener("keydown",(event)=>{
    console.log(document.getElementById("income").value)
    if (document.getElementById("income").value<10000){
        SUB.style.backgroundColor="#FFF3F3";
        SUB.disabled = true;
        SUB.style.cursor="not-allowed";
        document.getElementById("addIncome").innerHTML="Low income"
        document.getElementById("addIncome").style.display="inline"
    }
    else{
        document.getElementById("addIncome").style.display="none";
        SUB.disabled = false;
        SUB.style.cursor="pointer";
        SUB.style.backgroundColor="rgb(242,181,49)";
    }
})

document.getElementById("income").addEventListener("keyup",(event)=>{
    console.log(document.getElementById("income").value)
    if (document.getElementById("income").value<10000){
        SUB.style.backgroundColor="#FFF3F3";
        SUB.disabled = true;
        SUB.style.cursor="not-allowed";
        document.getElementById("addIncome").innerHTML="Low income"
        document.getElementById("addIncome").style.display="inline"
    }
    else{
        document.getElementById("addIncome").style.display="none";
        SUB.disabled = false;
        SUB.style.cursor="pointer";
        SUB.style.backgroundColor="rgb(242,181,49)";
    }
})





SUB.addEventListener("click",(event)=>{
    SUB.style.backgroundColor="#FFF3F3";
    SUB.disabled = true;
    SUB.style.cursor="not-allowed";
    console.log(income)
    MS=MSValue();
    CO=COValue();
    HO=COValue();
    
    income=document.getElementById("income").value;
    age=document.getElementById("age").value;
    experience=document.getElementById("experience").value;
    state=document.getElementById("statesId").value;
    currYears=document.getElementById("current_job_years").value;
    event.preventDefault();
    loader[0].style.opacity="1";
    fetch(`/test`,{
        headers : {
            'Content-Type' : 'application/json'
        },
        method : 'POST',
        body : JSON.stringify( {
            'MS':MS,
            'HO':HO,
            'CO':CO,
            'income':income,
            'age':age,
            'experience':experience,
            'state':state,
            'currYears':currYears
        })
    })
      .then(function (response) {
          return response.json();
      }).then(function (text) {
          console.log('GET response:');
          console.log(text["res"]); 
          if(text["res"]==1){
            loader[0].style.opacity="0";
            risk_1.style.display="block"
            setTimeout(() => {
            SUB.disabled = false;
            SUB.style.cursor="pointer";
            risk_1.style.display="none";
            SUB.style.backgroundColor="rgb(242,181,49)";
            }, 5000);
        }
        else{
            loader[0].style.opacity="0";
            risk_0.style.display="block"
            setTimeout(() => {
            SUB.disabled = false;
            SUB.style.cursor="pointer";
            risk_0.style.display="none";
            SUB.style.backgroundColor="rgb(242,181,49)";
            }, 5000);
        }
      });


    /*
    loader[0].style.opacity="1";
    risk_1.style.display="block";
    fetch('/adsd')
    .then((response) => {return response.json();
    }).then((myJson) => {
    console.log(myJson.result);
    if(myJson.result==1){
        loader[0].style.opacity="0";
        risk_1.style.display="block"
        setTimeout(() => {
        risk_1.style.display="none"
        }, 7000);
    }
    else{
        loader[0].style.opacity="0";
        risk_0.style.display="block"
        setTimeout(() => {
        risk_0.style.display="none"
        }, 7000);
    }
  });
 */
})







var txt ="";
var cpt =0;

function display()
{
	if (cpt >= txt.length){
    console.log(txt);
    return;
    }
	cpt++;
	var elt=document.getElementById("txt");
	var car = txt.substr(cpt,1);
	
	elt.innerHTML=elt.innerHTML+car;	
	
	setTimeout(display,100);	
}
function go()
{
	txt="You are Indian and you need credit ?... We are glad to help you";
	cpt = -1;
	document.getElementById("txt").innerHTML="";
	setTimeout(display(),10000);	
}

window.addEventListener("load", go);