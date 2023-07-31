console.log("HIIIIIIIIII");
console.log(window.location.href);

let cupcakeListData;
const $cupcakeListElement = $('#cupcake_list');
// console.log($cupcakeListElement);

// Function to get cupcakes data from the API
async function getAPICupcakesData() {
    try {
        let resp = await axios.get('/api/cupcakes');
        // console.log("Response= ", resp);
        // console.log("Response.data= ", resp.data);
        // console.log("Response.data.cupcakes= ", resp.data.cupcakes);
        return resp.data.cupcakes;
    } catch (error) {
        console.error('Error getting cupcakes:', error);
        return []; // Return an empty array instead
    }
}

async function render_cupcakes_list() {
	try {
		cupcakeListData = await getAPICupcakesData()
		$cupcakeListElement.empty();
        
		for (const cupcake of cupcakeListData) {
			console.log(cupcake);
			$cupcakeListElement.append(`
			<li>
				<div class="cupcake_wrapper">
					<p>&gt;</P>
					<img class="cupcake_img" src="${cupcake.image}" alt="Image of the cupcake could not be loaded.">
					<div class="cupcake_text">
						<p><b>Flavor:</b> ${cupcake.flavor} </p>
						<p><b>Size:</b> ${cupcake.size} </p>
						<p><b>Rating:</b> ${cupcake.rating}</p>
					</div>
				</div>
			</li>
			`);
		  }

    } catch (error) {
        console.error('Error trying to render cupcakes:', error);
    }

    
}


// Submit the cupcake form using Axios
$('#add_cupcake_form').submit(async function (event) {
    event.preventDefault();


	try {
		// Jquerry method to serialize form data
		const formDataArray = $(this).serializeArray();
		console.log("formDataArray=",formDataArray);
	
		// Convert the formDataArray to a dictionary (JavaScript object)
		const formDataPayload = formDataArray.reduce((input, { name, value }) => {
			
			// turing empty strings into null as to allow for a user to pass null to server
			if (name == "image" && value == ""){
				input[name] = null;
				return input;
			} else{
				input[name] = value;
				return input;
			}
	
		}, {});
		// console.log("formDataPayload=",formDataPayload);
	
		let resp = await axios.post('/api/cupcakes', formDataPayload);
		// console.log("Response= ", resp);
		// console.log("Response.data= ", resp.data);
	
		render_cupcakes_list()

    } catch (error) {
        console.error('Error trying to add a new cupcake:', error);
    }

});

render_cupcakes_list()