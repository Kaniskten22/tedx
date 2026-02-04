const qtyInput = document.getElementById("qty");
const totalText = document.getElementById("total");
const attendees = document.getElementById("attendees");

const PRICE = 1000;

qtyInput.addEventListener("input", () => {
    let qty = parseInt(qtyInput.value);
    if (qty < 1) qty = 1;

    totalText.innerText = qty * PRICE;
    attendees.innerHTML = "";

    for (let i = 1; i <= qty; i++) {
        attendees.innerHTML += `
        <div class="attendee">
            <input type="text" name="name[]" placeholder="Name ${i} (Required)" required>
            <input type="tel" name="phone[]" placeholder="Phone ${i} (Optional)">
            <input type="email" name="email[]" placeholder="Email ${i} (Optional)">
        </div>`;
    }
});
