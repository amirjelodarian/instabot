window.addEventListener('load',function(){

     


    const selectOption = document.getElementById('select');
    selectOption.addEventListener('click',function(){
        const hashtags = document.querySelector('.mainDivTagsCheckBoxs');
        const suggestion = document.querySelector('.mainDivSuggestion');
        switch(this.value){
            case 'likeOrFollowAsHashtags':
                while (suggestion.firstChild)
                     suggestion.firstChild.remove();
                hashtags.childElementCount == 0 ? createAddHashtagsContent() : '';
                break;
            case 'followSuggestionPeople':
                while (hashtags.firstChild) 
                    hashtags.firstChild.remove();
                suggestion.childElementCount == 0 ? createAddSuggestionContent() : '';
                break;
            default:
                alert('Values is wrong !');
                break;
            
        }
        
        
    });
   
    // for hashtags
    function createAddHashtagsContent(){

        const div = document.querySelector('.mainDivTagsCheckBoxs');
    

        const textarea = document.createElement('textarea');
        textarea.id = "addHashtags";
        textarea.className = "addHashtags"; 
        textarea.placeholder = "Separate each ','\nDon't use #"; 
        textarea.name = "addHashtags";

        const followCheckbox = document.createElement('input');
        followCheckbox.setAttribute('type','checkbox')
        followCheckbox.value = 'followTag';
        followCheckbox.name = 'followTag';
        followCheckbox.className = 'followTag';
        followCheckbox.id = 'followTag';

        const labelFollowCheckbox = document.createElement('label');
        labelFollowCheckbox.setAttribute('for','follow');
        labelFollowCheckbox.className = 'labelFollowTag';
        labelFollowCheckbox.innerHTML = 'Follow';

        const likeCheckbox = document.createElement('input');
        likeCheckbox.setAttribute('type','checkbox')
        likeCheckbox.value = 'likeTag';
        likeCheckbox.name = 'likeTag';
        likeCheckbox.className = 'likeTag';
        likeCheckbox.id = 'likeTag';

        const labelLikeCheckbox = document.createElement('label');
        labelLikeCheckbox.setAttribute('for','follow');
        labelLikeCheckbox.className = 'labelFollowTag';
        labelLikeCheckbox.innerHTML = 'Like';

        const countLikeOrFollow = document.createElement('input');
        countLikeOrFollow.setAttribute('type','number');
        countLikeOrFollow.name = 'countLikeOrFollow';
        countLikeOrFollow.className = 'countLikeOrFollow';
        countLikeOrFollow.placeholder = 'Count';
        countLikeOrFollow.innerHTML = '0';

        


        div.appendChild(labelFollowCheckbox);
        div.appendChild(followCheckbox);
        
        div.appendChild(labelLikeCheckbox);
        div.appendChild(likeCheckbox);
        
        div.appendChild(countLikeOrFollow);
        div.appendChild(textarea); 

    

        
    }

    // for suggestion
    function createAddSuggestionContent(){

        const div = document.querySelector('.mainDivSuggestion');
    

        const textarea = document.createElement('textarea');
        textarea.id = "addUserID";
        textarea.className = "addUserID"; 
        textarea.placeholder = "Separate each ','\nDon't use @"; 
        textarea.name = "addUserID";

        const countSuggestion = document.createElement('input');
        countSuggestion.setAttribute('type','number');
        countSuggestion.id = 'countSuggestion';
        countSuggestion.className = 'countLikeOrFollow';
        countSuggestion.name = 'countSuggestion';
        countSuggestion.placeholder = 'Count';
        countSuggestion.innerHTML = '0';

        const labelCount = document.createElement('label');
        labelCount.setAttribute('for','countSuggestion');
        labelCount.className = 'labelCountSuggestion';
        labelCount.innerHTML = 'Count';

        div.appendChild(labelCount);
        div.appendChild(countSuggestion);
        div.appendChild(textarea); 

        
    }

});

