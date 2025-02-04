function compressImage() {
    let fileInput = document.getElementById("imageInput");
    let sizeInput = document.getElementById("size");
    let unitInput = document.getElementById("unit");
    let message = document.getElementById("message");

    if (fileInput.files.length === 0) {
        message.textContent = "Please select an image.";
        return;
    }

    let formData = new FormData();
    formData.append("image", fileInput.files[0]);
    formData.append("size", sizeInput.value);
    formData.append("unit", unitInput.value);

    fetch("/compress", {
        method: "POST",
        body: formData,
    })
    .then(response => response.blob())
    .then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "compressed_image.jpg";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        message.textContent = "Image compressed successfully!";
    })
    .catch(error => {
        console.error("Error:", error);
        message.textContent = "Compression failed.";
    });
}
