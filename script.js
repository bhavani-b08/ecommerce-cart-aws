const API_URL = "https://2jd3pn8h0g.execute-api.ap-south-1.amazonaws.com/dev";

function getUserId() {
    return localStorage.getItem("userId") || "User123";  // Get userId dynamically
}

function updateCartCount() {
    fetch(`${API_URL}/getCartCount?userId=${getUserId()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("cart-count").innerText = data.cartCount || 0;
        })
        .catch(error => {
            console.error("Error fetching cart count:", error);
        });
}

function addToCart(productId) {
    fetch(`${API_URL}/addToCart`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            userId: getUserId(), 
            productId: productId, 
            quantity: 1 
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data);
        alert(data.message || "Item added to cart!");
        updateCartCount();
    })
    .catch(error => {
        console.error("Error adding to cart:", error);
        alert("Failed to add item: " + error.message);
    });
}    


function removeFromCart(productId) {
    fetch(`${API_URL}/removeFromCart`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Accept": "application/json" // Ensure proper JSON response
        },
        body: JSON.stringify({ userId: getUserId(), productId: productId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || "Item removed from cart.");
        updateCartCount();
    })
    .catch(error => {
        console.error("Error removing from cart:", error);
        alert("Failed to remove item.");
    });
}

document.addEventListener("DOMContentLoaded", updateCartCount);
