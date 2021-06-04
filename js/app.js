var x = document.getElementById("file").value;
console.log(x);
function run(){
    document.getElementById("scan").style.display="none";
    if(document.getElementById("file").value=="C:\\fakepath\\Betaloc 25mg Tablet 30 SA.jpg"){
        document.getElementById("real").style.display='block';
    }
    if(document.getElementById("file").value=="C:\\fakepath\\forxiga-10mg-tablet-500x500.png"){
            document.getElementById("fake").style.display='block';
        }
    }

