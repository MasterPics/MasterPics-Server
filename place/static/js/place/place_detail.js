//Save
const onClickSave = async (place_id) => {
    try {
        // const url = '/place/';
        // const {
        //     data
        // } = await axios.post(url, {
        //     place_id,
        // })
        // modify(data.place_id, data.is_saved)

        const options = {
            url: '/place/save/',
            method: 'POST',
            data: {
                place_id: place_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
            modify(data.place_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

const modify = (place_id, is_saved) => {
    const save = document.querySelector(`.save-${place_id} i`);
    const save_content = document.querySelector(`.save-${place_id} .save__content`)
    const num = save_content.innerText; // [ {{ place.save_users.count }} ]
    console.log(num)
    if (is_saved === true) {

        save.className = "fas fa-bookmark";

        const count = Number(num) + 1;
        save_content.innerHTML = count
    } else {
        save.className = "far fa-bookmark";

        const count = Number(num) - 1;
        save_content.innerHTML = count
    }

}


const modifyNewComment = (place_id, comment_id, value) => {
    const CommentContainer = document.querySelector(`.comments-${place_id}`);
    console.log(CommentContainer)

    const tempContainer = document.createElement("div");
    tempContainer.className = `comment comment-${comment_id}`;


    tempContainer.textContent = value;

    const deleteBtn = document.createElement("input");
    deleteBtn.className = "comment-btn";
    deleteBtn.setAttribute("type", "submit");
    deleteBtn.setAttribute("value", "삭제");
    deleteBtn.setAttribute("onclick", `onClickDeleteComment(${comment_id})`)

    tempContainer.appendChild(deleteBtn);
    CommentContainer.appendChild(tempContainer);
}

const onClickNewComment = async (id) => {
    const url = `/place/${id}/comment_create/`;
    const value = document.querySelector(`.createComment-${id} .comment__value`);
    const value_text = value.value
    const {
        data
    } = await axios.post(url, {
        id,
        value: value_text
    })

    modifyNewComment(id, data.comment_id, data.value);
}

const modifyDeleteComment = (comment_id) => {

    const targetCommentContainer = document.querySelector(`.comment-${comment_id}`);
    targetCommentContainer.remove();
}

const onClickDeleteComment = async (comment_id) => {
    const url = `/place/${comment_id}/comment_delete/`;

    const {
        data
    } = await axios.post(url, {
        comment_id
    })
    modifyDeleteComment(data.comment_id);
}