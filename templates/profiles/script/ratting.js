function calculateRating() {
    let successfulCases = parseFloat(document.getElementById('successful_cases').value);
    let unsuccessfulCases = parseFloat(document.getElementById('unsuccessful_cases').value);
    let experience = parseFloat(document.getElementById('experience').value);

    let rating = (successfulCases - unsuccessfulCases) * Math.sqrt(1 + experience);
    document.getElementById('rating').innerText = "Ratting: " + rating.toFixed(2);
}

calculateRating()