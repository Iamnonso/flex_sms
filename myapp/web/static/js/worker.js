//if candidate select the state of origin
const selectState = document.getElementById('stud_state');
const selectCity = document.getElementById('stud_city');

selectState.addEventListener('change', (event) => {
    event.preventDefault();
    const state = selectState.value;
    selectCity.innerHTML = '<option value="">Please wait...</option>';
    $.ajax({
        url: `/cities/${state}`,
        type: 'GET',
        success: (data) => {
            console.log(data.response);
            const cities = data.response;
            selectCity.innerHTML = '<option value="">Select City</option>';
            cities.forEach(city_name => {
                const option = document.createElement('option');
                option.value = city_name;
                option.textContent = city_name;
                selectCity.appendChild(option);
            });
        },

        fail: (error) => {
            selectCity.innerHTML = '<option value="">Select City</option>';
            console.log(error);
        }
    });




});