

// retrieve
// let token = localStorage.getItem('jwtToken');



            // Initialize some variables
            let nextPage = 0;

            // trial for userInput
            let userInput_previous = '';
            let userInput = '';
            let isLoading = false;

            // Function to fetch data

            // function fetchData1111111() {
            // // Check if data is currently being loaded
            // if (isLoading) return;
            // isLoading = true;

            // fetch(`http://127.0.0.1:3000/api/attractions?page=${nextPage}`)
            //     .then(response => response.json())
            //     .then(data => {
            //     const dataContainer = document.getElementById('part2_twelve');
            //     const newData = data.data;

            //     // Append the new data to the container
            //     newData.forEach(item => {
            //         const newItem = document.createElement('div');
            //         newItem.textContent = item.name; // Modify this to match your data structure
            //         dataContainer.appendChild(newItem);
            //     });

            //     // Update nextPage value
            //     nextPage = data.nextPage;

            //     isLoading = false; // Reset loading flag
            //     })
            //     .catch(error => {
            //     console.error('Error fetching data:', error);
            //     isLoading = false; // Reset loading flag in case of error
            //     });
            // }

            // Function to check if the user has scrolled to the bottom
            // you could watch 5 people or just one of them

            // entries[0] the first observed object.
            function checkIntersection(entries) {
            if (entries[0].isIntersecting) {
                if (nextPage != null) {
                    get_data_12();
                }
            }
            }

            // In the context of the Intersection Observer, 
            // entries will be an array of IntersectionObserverEntry objects 

            // isIntersecting is a property of an IntersectionObserverEntry object. 
            // It's a boolean value that indicates whether the observed element is currently 
            // intersecting with the root element (viewport or other container).

            // Set up Intersection Observer
            const observer = new IntersectionObserver(checkIntersection, { threshold: 1 });
            //  (in this case, threshold: 1 meaning the entire element is within the viewport)
            // the Intersection Observer will trigger the checkIntersection callback function

            const triggerElement = document.getElementById('intersection-trigger');
            observer.observe(triggerElement);


            //      .to watch (this guy) -> see if fully within the viewport
            // 



            const hostname = window.location.hostname;
            // when hostname is used below before ":3000", it does not work on local PC...

            fetch('/api/mrts')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('container');

                    data.data.forEach((name, index) => {
                        if (name !== "No MRT station") {
                            const div = document.createElement('div');
                            div.classList.add("body_body_medium");
                            div.textContent = name;
                            // div.classList.add('list_item');
                            container.appendChild(div);
                        }
                    });
                })
                .catch(error => console.error('Error:', error));



            const list = document.querySelector('.list');
            const leftButton = document.getElementById('left_arrow');
            const rightButton = document.getElementById('right_arrow');
            const itemWidth = 90; // Adjust as needed (includes width + margin-right)
            const itemsToShow = 10; // Number of items to show at a time

            let currentPosition = 0;
            const moveDistance = itemWidth * 3; // Increase the increment value

            rightButton.addEventListener('click', () => {
                if (currentPosition > -itemWidth * (list.children.length - itemsToShow)) {
                    currentPosition -= moveDistance;
                    list.style.transform = `translateX(${currentPosition}px)`;
                }
            });

            leftButton.addEventListener('click', () => {
                if (currentPosition < 0) {
                    currentPosition += moveDistance;
                    list.style.transform = `translateX(${currentPosition}px)`;
                }
            });




            document.addEventListener('DOMContentLoaded', function() {
                let listItems = document.querySelectorAll('.list_bar_container div');

                // Function to handle mouse over event
                function handleMouseOver(element) {
                    element.addEventListener('mouseover', function() {
                        element.style.color = '#000';
                    });
                }

                // Function to handle mouse out event
                function handleMouseOut(element) {
                    element.addEventListener('mouseout', function() {
                        element.style.color = '#666';
                    });
                }

                // Add event listeners for each list item
                listItems.forEach(function(item) {
                    handleMouseOver(item);
                    handleMouseOut(item);
                });
            });


            document.addEventListener('DOMContentLoaded', function() {
                // Get the arrow elements
                let leftArrow = document.getElementById('left_arrow');
                let rightArrow = document.getElementById('right_arrow');

                // Define the hovered image sources
                let leftHoveredImageSrc = '/static/images/arrow_left_hovered.png';
                let rightHoveredImageSrc = '/static/images/arrow_right_hovered.png';

                // Define the original image sources
                let leftOriginalImageSrc = '/static/images/arrow_left.png';
                let rightOriginalImageSrc = '/static/images/arrow_right.png';

                // Function to handle mouse over event
                function handleMouseOver(element, hoveredSrc) {
                    element.addEventListener('mouseover', function() {
                        element.querySelector('img').src = hoveredSrc;
                    });
                }

                // Function to handle mouse out event
                function handleMouseOut(element, originalSrc) {
                    element.addEventListener('mouseout', function() {
                        element.querySelector('img').src = originalSrc;
                    });
                }

                // Add event listeners for left arrow
                handleMouseOver(leftArrow, leftHoveredImageSrc);
                handleMouseOut(leftArrow, leftOriginalImageSrc);

                // Add event listeners for right arrow
                handleMouseOver(rightArrow, rightHoveredImageSrc);
                handleMouseOut(rightArrow, rightOriginalImageSrc);
            });



            function get_data_12() {
                // Check if data is currently being loaded
                if (isLoading) return;
                isLoading = true;
                
                fetch(
                `http://${hostname}:3000/api/attractions?page=${nextPage}&keyword=${userInput}`
                )
                
                .then(function (response) {
                return response.json();
                })
                
                .then(function (data) {
                let result = document.querySelector("#part2_twelve");
                let attractions = data.data; // Access the 'results' property

                // Check if data is empty
                if (attractions.length === 0) {
                    let noResultElement = document.createElement("div");
                    noResultElement.classList.add("body_body_medium");
                    noResultElement.textContent = "No Result!";
                    result.appendChild(noResultElement);
                
                } else {
                // Update nextPage value
                nextPage = data.nextPage;

                for (let i = 0; i < 12 && i < attractions.length; i++) {
                    let attraction = attractions[i];

                    let attractionElement = document.createElement("div");
                    attractionElement.classList.add("sight");


                    attractionElement.setAttribute("id", attraction.id);
                    

                    let box1 = document.createElement("div"); // trial  
                    box1.classList.add("img_box");

                    let box3 = document.createElement('a');
                    box3.classList.add("invisible-link");
                    box3.href = "/attraction/" + attraction.id;
                    

                    
                    let imageElement = document.createElement("img");
                    imageElement.src = getFirstJpgUrl(attraction.images[0]);
                    box3.appendChild(imageElement);

                    box1.appendChild(box3);

                    
                    

                    let overlayElement = document.createElement("div");
                    overlayElement.classList.add("overlay");
                    overlayElement.classList.add("body_body_bold");

                    overlayElement.textContent = attraction.name;

                    box1.appendChild(overlayElement);  
                        
                    attractionElement.appendChild(box1);      // trial

                    let box2 = document.createElement("div"); // trial 
                    box2.classList.add("title_box");
                    
                    
                    let titleElement = document.createElement("div");
                    titleElement.classList.add("title_box_left");
                    titleElement.classList.add("body_body_medium");
                    
                    titleElement.textContent = attraction.mrt;

                    let titleElement_right = document.createElement("div");
                    titleElement_right.classList.add("title_box_right");
                    titleElement_right.classList.add("body_body_medium");
                    titleElement_right.textContent = attraction.category;

                    box2.appendChild(titleElement);
                    box2.appendChild(titleElement_right);
                    


                    // let box_left = document.createElement("div"); // trial on left-right
                    // let rightElement = document.createElement("div");
                    // leftElement.classList.add("title_box_left");
                    // leftElement.textContent = attraction.stitle;
                    // box_left.appendChild(leftElement);
                    // titleElement.appendChild(box_left);



                    attractionElement.appendChild(box2);      // trial
                    result.appendChild(attractionElement);
                }


                }
                // Reset loading flag
                isLoading = false;
                })
                
                .catch(function (error) {
                console.log("Error:", error);
                });
            }            




      
            function getFirstJpgUrl(string) {
                let pattern = /https?:\/\/[^\s]+?\.[jJ][pP][eE]?[gG]/;
                let matches = string.match(pattern);
        
                if (matches) {
                return matches[0];
                } else {
                return "No JPEG URL found in the string.";
                }
            }

            document.addEventListener('DOMContentLoaded', function() {
                const searchInput = document.getElementById('search-input');
                const searchButton = document.querySelector('.search-button');
                const dataContainer = document.getElementById('part2_twelve');

                // searchInput.addEventListener('input', performSearch);
                
                searchButton.addEventListener('click', performSearch);
                
                // function performSearch() {
                //     if (nextPage === null) return;
                //     userInput = searchInput.value;
                //     const url = `http://127.0.0.1:3000/api/attractions?page=${nextPage}&keyword=${userInput}`;

                //     fetch(url)
                //         .then(response => response.json())
                //         .then(data => {
                //             // Clear existing data
                //             dataContainer.innerHTML = '';
                            
                //             // Process and display new data
                //             let attractions = data.data;

                //             // nextPage = 0

                //             get_data_12(attractions); // Reuse the existing function
                //         })
                //         .catch(error => console.error('Error:', error));
                // }

                function performSearch() {
                    userInput = searchInput.value;
                    if (userInput !== userInput_previous) {
                        nextPage = 0
                    } 

                    if (nextPage === null) return;
                    dataContainer.innerHTML = '';
                    userInput_previous = userInput;
                    get_data_12();
                    
                }
            });


            window.addEventListener('load', function() {
                // Your event listener registration code here

                // Get the list container
                let listContainer = document.querySelector('.list');

                // Function to handle mouse over event
                function handleMouseOver(event) {
                    let target = event.target;

                    if (target.tagName === 'DIV' && target.parentElement.classList.contains('list')) {
                        target.style.color = '#000';
                    }
                }

                // Function to handle mouse out event
                function handleMouseOut(event) {
                    let target = event.target;

                    if (target.tagName === 'DIV' && target.parentElement.classList.contains('list')) {
                        target.style.color = '#666';
                    }
                }

                // Function to handle click event
                function handleClick(event) {
                    let target = event.target;
                    const dataContainer = document.getElementById('part2_twelve');

                    if (target.tagName === 'DIV' && target.parentElement.classList.contains('list')) {
                        
                        userInput = target.textContent; // Get the text content of the clicked div

                        // input the sight name into search bar:
                        const searchInput = document.getElementById('search-input');
                        searchInput.value = target.textContent;
                        
                        if (userInput !== userInput_previous) {
                            nextPage = 0
                        } 

                        if (nextPage === null) return;

                        dataContainer.innerHTML = '';
                        get_data_12();
                        userInput_previous = userInput;
                    }
                }

                // Attach event listeners to the list container
                listContainer.addEventListener('mouseover', handleMouseOver);
                listContainer.addEventListener('mouseout', handleMouseOut);
                listContainer.addEventListener('click', handleClick);
            });


            
            document.addEventListener('click', function(event) {
                let clickedElement = event.target;

                if (clickedElement.classList.contains('sight')) {
                    let selectedId = clickedElement.id;
                    console.log("Selected ID:", selectedId);
                }
            });

