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
        dataType: 'json',
        success: (data) => {
            console.log(data);
            selectCity.innerHTML = '<option value="">Select City</option>';
            data.forEach(state_name => {
                const option = document.createElement('option');
                option.value = state_name;
                option.textContent = state_name;
                selectCity.appendChild(option);
            });
        },

        fail: (error) => {
            selectCity.innerHTML = '<option value="">Select City</option>';
            console.log(error);
        }
    });




});