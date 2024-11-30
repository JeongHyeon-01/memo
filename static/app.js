async function deleteMemo(event) {
  const id = event.target.dataset.id;
  const res = await fetch(`/memo/${id}`, {
    method :'DELETE',
  });
  readMemo();
}

async function editMemo(event){
  const id = event.target.dataset.id;
  const editInput = prompt('수정할 값을 입력하세요~!');
  const res = await fetch(`/memo/${id}`, {
    method :'PUT',
    headers:{
      "Content-Type" : "application/json"
    },
    body:JSON.stringify({
      id : id,
      content : editInput
    })
  });
  readMemo();
}

function displayMemo(memo){
  const ul = document.querySelector("#memo-ul");
  const li = document.createElement("li");
  console.log(memo)
  li.innerText = `[id:${memo.id}] ${memo.content}`
  const editBtn = document.createElement("button");
  
  
  editBtn.innerText = '수정하기';
  editBtn.addEventListener("click", editMemo);
  editBtn.dataset.id = memo.id

  const delBtn = document.createElement("button");
  delBtn.innerText = '삭제하기';
  delBtn.addEventListener("click", deleteMemo);
  delBtn.dataset.id = memo.id

  ul.appendChild(li);
  li.appendChild(editBtn);
  li.appendChild(delBtn);
}

async function readMemo(){
  const res = await fetch('/memos')
  const jsonRes = await res.json();
  const ul = document.querySelector("#memo-ul");
  ul.innerHTML = "";
  jsonRes.forEach(displayMemo);
}

async function createMemo(value){
  const res = await fetch("/memos", {
    method :'POST',
    headers:{
      "Content-Type" : "application/json"
    },
    body:JSON.stringify({
      id : new Date().getTime(),
      content : value
    })
  });
  readMemo();
}

function handleSubmit(event){
  event.preventDefault();
  const input = document.querySelector('#memo-input');
  createMemo(input.value)
  input.value =""  
}



const form = document.querySelector('#memo-form');
form.addEventListener("submit", handleSubmit);

readMemo();