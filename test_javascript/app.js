

// $searchList = $('#search-list')
// $searchList.on('click', 'li', selectFood)
SELECTED_FOODS = []


async function handlesubmit(evt){
    evt.preventDefault()
    let id = $('#food').val()

    try{
        let resp = await axios.get(
            `https://api.nal.usda.gov/fdc/v1/food/${id}?api_key=4JD1xo6rlkekDofsraPVxEPMFX2aYCB5NpTUR47O`)
        console.log(resp)
        // displayResults(resp.data)
    }
    catch(error){
    
    }
}

$('#search').on('submit', handlesubmit)

// function displayResults(resp){
//     $searchList.empty()
//     for (food of resp.foods){
//         $item = $(<li class="list-group-item" data-id=${food.fdcId}>${food.description}<br>
//             <small class="text-muted" data-id=${food.fdcId}>${food.ingredients}</small></li>)
//         $searchList.append($item)
//         }
// }

// function selectFood(evt){
    
//     if (SELECTED_FOODS.length < 4){
//         $(evt.target).addClass('bg-info')
//         SELECTED_FOODS.push($(evt.target).attr('data-id'))
//         $('#meal-list').append($(evt.target))
//     }

//     if (SELECTED_FOODS.length === 4){
//         $("input[name='food-ids']").val(SELECTED_FOODS)
//     }
   
//     console.log(SELECTED_FOODS)
// }
