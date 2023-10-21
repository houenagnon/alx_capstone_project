const searchInput = document.getElementById("searchBox");
const listContainer = document.getElementById("list-container");

const firstContainer = document.getElementById("body_container");
const secondContainer = document.getElementById("body_container1");

const addButton = document.getElementById("add_button");
const returnButton = document.getElementById("return_button");

let taskBody = document.getElementById("task-body");


let tasks = document.querySelectorAll(".task");


function creer_task(){
    firstContainer.style.display = "none";
    addButton.style.display = "none";
    returnButton.style.display = "block";
    secondContainer.style.display = "block";
    
}

function list_task(){
    firstContainer.style.display = "block";
    addButton.style.display = "block";
    returnButton.style.display = "none";
    secondContainer.style.display = "none";
    location.reload(true);
}


function save_task(){
    const taskName = document.getElementById("task_name").value;
    const taskDescription = document.getElementById("task_desc").value;
    const taskStatus = document.getElementById("task_status").value;
    const taskDate = document.getElementById("task_date").value;

    if(taskName === '' || taskStatus ==='' || taskDate===''|| taskDescription===''){
        alert("Champs Vide!!!");
    }else{

        // document.getElementById("task_name").value = "";
        // document.getElementById("task_status").value = "";
        const data = {
            id: window.localStorage.getItem("how"),
            name: taskName,
            content: taskDescription,
            tag: taskStatus,
            due_date: taskDate
          };
          console.log(data)
          
        fetch('http://127.0.0.1:5000/task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Task save : ', data);

            if (data)
            {
                let div = document.createElement("div");
                div.setAttribute("id", data.id)
                div.innerHTML = taskName;
                //console.log(taskName + ":::::::");
                taskBody.appendChild(div);
                
                
                if(taskStatus==="en_cours"){
                    div.classList.add("task", "color2");
                }else if(taskStatus === "termine"){
                    div.classList.add("task", "color3");
                }else{
                    div.classList.add("task", "color1");
                }
            }
            else
                alert(data.msg);


            returnButton.style.display = "none";
            secondContainer.style.display = "none";
            firstContainer.style.display = "block";
            addButton.style.display = "block";
            
        })
        .catch((error) => {
            console.error('Une erreur s\'est produite lors de l\'enregistrement de l\'utilisateur : ', error);
        });

     }
}






taskBody.addEventListener("click", function(e){
    if(e.target.classList.contains("task")){
         // L'élément cliqué a la classe "task"
         const id = e.target.getAttribute("id");
         let childDiv = e.target.querySelector("div.additional-content");

         // Vérifiez si l'élément enfant existe
         if (childDiv) {
             // L'élément enfant existe, supprimez-le
            
             childDiv.remove();
         } else {
             // L'élément enfant n'existe pas, ajoutez-le
             childDiv = document.createElement("div");
             childDiv.classList.add("additional-content");
             
             let editImg = document.createElement("img");
             editImg.src = "images/edit.png";
             editImg.alt = "Edit";
 
             let closeImg = document.createElement("img");
             closeImg.src = "images/close.png";
             closeImg.alt = "Close";
             
              // Ajoutez un gestionnaire d'événements onclick à l'image "Edit"
            editImg.onclick = function() {
                creer_task();
                // Utilisez textContent pour obtenir le texte actuel
                let texteActuel = e.target.textContent;
                let statusActuel = e.target.classList[1];
                

                // alert(statusActuel);
                document.getElementById("task_name").value = texteActuel.trim();

                if(statusActuel === 'color1'){
                    document.getElementById("task_status").selectedIndex = 1;
                }else if(statusActuel === 'color2'){
                    document.getElementById("task_status").selectedIndex = 2;
                }else{
                    document.getElementById("task_status").selectedIndex = 3;
                }
                console.log('Id est ------------> ' + id)
                // A completer .........................................
                fetch('http://localhost:5000/task/by/' + id, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'  
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    document.getElementById('task_desc').value = data[0].content
                    document.getElementById('task_date').value = data[0].due_date
                })
                .catch(error => console.error('Erreur :', error));
                

                document.getElementById("save_button").onclick =    function(){
                    const taskName = document.getElementById("task_name").value;
                    const taskDescription = document.getElementById("task_desc").value;
                    const taskDate = document.getElementById("task_date").value;
                    const TS = document.getElementById("task_status").value;

                    const updatedTask = {
                        name: taskName,
                        content: taskDescription,
                        tag: TS,
                        due_date: taskDate
                    };
                    
                    fetch('http://localhost:5000/task/' +id, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(updatedTask)
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erreur lors de la mise à jour de la tâche');
                        }
                        return response.json();
                    })
                    .then(data =>{ console.log(data)
                        list_task();
                    })
                    .catch(error => console.error('Erreur :', error.message));
                    
                };
            };

            // Ajoutez un gestionnaire d'événements onclick à l'image "Close"
            closeImg.onclick = async function() {

                await fetch("http://localhost:5000/task/"+id, {
                            method: "DELETE",
                            headers: {
                                "Content-Type": "application/json"
                            }
                        }).then((data)=> data.json()).then(data => {
                            console.log(data);
                            e.target.remove();
                        })
               
            };
             childDiv.appendChild(editImg);
             childDiv.appendChild(closeImg);
 
             e.target.appendChild(childDiv);
        }
    }
    else if(e.target.tagName === "SPAN"){
        e.target.remove();
        saveData();
    }
}, false);


function save_user(){
    // window.location.href = "index.html";
    const name = document.getElementById("user_name").value;
    const email = document.getElementById("user_mail").value;
    const pass = document.getElementById("user_pass").value;
    const pass1 = document.getElementById("user_pass1").value;
    
    let msg_error = document.getElementById("msg_error");
    if(name == ' ' || email == '' || pass == ' '){
        msg_error.textContent = "All the input are not filled"
    }

    if(pass != pass1){

        msg_error.textContent = "Password not matched"
    }

    const data = {
        username: name,
        email: email,
        password: pass
    };
    
    fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Utilisateur enregistré avec succès : ', data);
            window.location.href = "connect.html"
        })
        .catch((error) => {
            console.error('Une erreur s\'est produite lors de l\'enregistrement de l\'utilisateur : ', error);
        });
}

function connect_user(){
    const email = document.getElementById("user_mail_c").value.trim();
    const pass = document.getElementById("user_pass_c").value;


    const data = {
        email: email,
        password: pass
    };

    fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            // const dataB = JSON.parse(data);
            console.log('Utilisateur Connecté avec succès : ', data);
            window.localStorage.setItem("username", data.username);
            window.localStorage.setItem("access_token", data.access_token);
            window.localStorage.setItem("how", data.how);

            
            window.location.href = "index.html";
        })  
        .catch((error) => {
            console.error('Une erreur s\'est produite lors de l\'enregistrement de l\'utilisateur : ', error);
        });
   
            
        
}

function deconnect(){
    window.localStorage.removeItem("access_token");
    window.localStorage.removeItem("username");
    window.localStorage.removeItem("how");
    window.location.href = "connect.html";
}

function go_to_connect(){
    window.location.href = "connect.html";
}

// function saveData(){
//     localStorage.setItem("data", listContainer.innerHTML);
// }

// function showTask(){
//     listContainer.innerHTML = localStorage.getItem("data");
// }

function filter(){
    const critere = searchInput.value.toLowerCase();
    const items = taskBody.getElementsByTagName("div");


    for (let i = 0; i < items.length; i++) {
        const texteItem = items[i].textContent.toLowerCase();

        if (texteItem.includes(critere)) {
            items[i].style.display = 'block'; // Afficher l'élément
        } else {
            items[i].style.display = 'none'; // Masquer l'élément
        }
    }
}


searchInput.addEventListener('input', filter);

// showTask();
// 

// A faire :
// ---- Creer la manière de Supprimer et de modifier
// ---- Voir la manière de mettre un label pour les status
// ---- Connecion avec un server pour communication


