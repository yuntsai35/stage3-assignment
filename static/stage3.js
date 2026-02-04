async function upload(){
    const fileInput = document.querySelector("#file");
    const textInput = document.querySelector("#text");
    
    if( fileInput.files.length == 0 & textInput.value == ""){
        alert("請輸入文字或檔案");
        return;
    }
    const formData = new FormData();
    formData.append("text", textInput.value); 
    formData.append("file", fileInput.files[0]);


    let response=await fetch("/files",{
        method:"POST",
        body: formData
    });
    let result = await response.json();

    if(response.ok){
       location.reload();
    }
}

async function render_content(){
    let response=await fetch("/files",{
        method:"GET",
    });

    const result = await response.json();
    result.data.forEach((data) => {
        const container = document.querySelector(".bottom");
    
        const post= document.createElement("div");
        post.className = "post";
        post.innerHTML = `
                    <hr>
                    <div class="post-container">
                    <div class="post-word">${data.content}</div>
                    <img class="post-picture" src="${data.picture}">
                    </div>
            `;
        container.appendChild(post);

})
    
}
render_content();