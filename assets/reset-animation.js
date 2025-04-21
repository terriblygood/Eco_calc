console.log("Скрипт инициализирован");

let carTop, carBottom, calculateBtn, roomsInput;

const checkElementsLoaded = setInterval(() => {
    carTop = document.getElementById("car-top");
    carBottom = document.getElementById("car-bottom");
    calculateBtn = document.getElementById("calculate-btn");
    roomsInput = document.getElementById("rooms");

    if (carTop && carBottom && calculateBtn && roomsInput) {
        clearInterval(checkElementsLoaded);
        console.log("Элементы найдены:", { carTop, carBottom, calculateBtn, roomsInput });

        calculateBtn.addEventListener("click", () => {
            const roomsValue = parseFloat(roomsInput.value);
            const isValid = !isNaN(roomsValue) && roomsValue >= 10 && roomsValue <= 1000;

            if (!isValid) {
                console.log("Некорректное значение. Вибрация.");
                calculateBtn.classList.add("shake");

                setTimeout(() => {
                    calculateBtn.classList.remove("shake");
                }, 300);
                return;
            }

            // Если всё ок — "спокойный" клик
            calculateBtn.classList.add("calm-click");
            setTimeout(() => {
                calculateBtn.classList.remove("calm-click");
            }, 500);

            [carTop, carBottom].forEach((car, idx) => {
                if (car) {
                    car.style.transition = "none";
                    car.style.left = "0px";
                    car.offsetHeight; // принудительный reflow
                    setTimeout(() => {
                        car.style.transition = "left 4s ease-in-out";
                        car.style.left = "100%";
                        console.log(`Машина ${idx + 1} поехала`);
                    }, 50);
                }
            });
        });
    }
}, 200);
