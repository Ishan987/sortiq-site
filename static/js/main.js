document.addEventListener('DOMContentLoaded', () => {
    // Slider Implementation
    const slider = document.querySelector('.hero-slider');
    const slides = document.querySelectorAll('.hero-slider .slide');
    let currentSlide = 0;
    let sliderInterval;
    const slideDuration = 4000; // 4s slide duration is standard for readable content
    let isPaused = false;
    
    function nextSlide() {
        if (isPaused) return;
        if (slides.length > 0) {
            slides.forEach(slide => slide.classList.remove('prev'));
            const oldSlide = slides[currentSlide];
            currentSlide = (currentSlide + 1) % slides.length;
            const newSlide = slides[currentSlide];
            
            oldSlide.classList.remove('active');
            oldSlide.classList.add('prev');
            newSlide.classList.add('active');
        }
    }

    function prevSlide() {
        if (slides.length > 0) {
            slides.forEach(slide => slide.classList.remove('prev'));
            const oldSlide = slides[currentSlide];
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            const newSlide = slides[currentSlide];
            
            oldSlide.classList.remove('active');
            newSlide.classList.add('active');
        }
    }

    function resetAutoPlay() {
        clearInterval(sliderInterval);
        sliderInterval = setInterval(nextSlide, slideDuration);
    }

    if (slides.length > 0) {
        slides[0].classList.add('active');
        sliderInterval = setInterval(nextSlide, slideDuration);

        if (slider) {
            slider.addEventListener('mouseenter', () => {
                isPaused = true;
            });
            slider.addEventListener('mouseleave', () => {
                isPaused = false;
            });
        }

        const prevControl = document.querySelector('.prev-control');
        const nextControl = document.querySelector('.next-control');

        if (prevControl) {
            prevControl.addEventListener('click', (e) => {
                e.stopPropagation();
                prevSlide();
                resetAutoPlay();
            });
        }

        if (nextControl) {
            nextControl.addEventListener('click', (e) => {
                e.stopPropagation();
                nextSlide();
                resetAutoPlay();
            });
        }
    }

    // Counter animations (High Performance / Zero Lag)
    const counters = document.querySelectorAll('.counter-number');
    const duration = 2000; // duration of animation in ms

    const animateCounters = () => {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            let start = null;

            const step = (timestamp) => {
                if (!start) start = timestamp;
                const progress = Math.min((timestamp - start) / duration, 1);
                // Quadratic ease-out formula
                const easeOut = progress * (2 - progress);
                counter.innerText = Math.floor(easeOut * target) + '+';
                
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    counter.innerText = target + '+';
                }
            };
            window.requestAnimationFrame(step);
        });
    };

    // Trigger counters when scrolled into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                const items = entry.target.querySelectorAll('.counter-item');
                items.forEach((item, index) => {
                    item.style.transitionDelay = `${index * 120}ms`;
                    item.classList.add('revealed');
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.05 });

    const counterSection = document.querySelector('.counter-section');
    if (counterSection) {
        observer.observe(counterSection);
    }

    // YouTube Facade Click Loader
    const facades = document.querySelectorAll('.youtube-facade');
    facades.forEach(facade => {
        facade.addEventListener('click', function(e) {
            const videoId = this.getAttribute('data-video-id');
            this.innerHTML = `<iframe width="100%" height="100%" src="https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1" style="border:0; width:100%; height:100%; position:absolute; top:0; left:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
        });
    });

    // Modal Handling
    const modals = document.querySelectorAll('.modal');
    const triggers = document.querySelectorAll('[data-toggle="modal"]');
    const closes = document.querySelectorAll('.modal .close');

    triggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = trigger.getAttribute('data-target');
            const targetModal = document.querySelector(targetId);
            if (targetModal) {
                targetModal.style.display = 'flex';
            }
        });
    });

    closes.forEach(close => {
        close.addEventListener('click', () => {
            close.closest('.modal').style.display = 'none';
        });
    });

    window.addEventListener('click', (e) => {
        modals.forEach(modal => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Form Handling (AJAX)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const action = form.getAttribute('action');
            const formData = new FormData(form);

            fetch(action, {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                form.reset();
                const modal = form.closest('.modal');
                if (modal) {
                    modal.style.display = 'none';
                }
            })
            .catch(err => {
                console.error(err);
                alert('An error occurred. Please try again.');
            });
        });
    });

    // Testimonials Slider Implementation
    const thumbs = document.querySelectorAll('.single-bio-thumb');
    const testimonials = document.querySelectorAll('.single-testimonial');
    let currentTestimonialIndex = 0;
    let testimonialInterval;
    let isTestimonialPaused = false;

    function showTestimonial(index) {
        testimonials.forEach((t) => {
            t.style.display = 'none';
            t.classList.remove('active');
        });

        const total = thumbs.length;
        const prevIndex = (index - 1 + total) % total;
        const nextIndex = (index + 1) % total;

        thumbs.forEach((thumb, i) => {
            thumb.classList.remove('active');
            const img = thumb.querySelector('.bio-image img');
            const name = thumb.querySelector('.bio-name');
            
            if (i === index || i === prevIndex || i === nextIndex) {
                thumb.style.display = 'flex';
                if (i === prevIndex) {
                    thumb.style.order = '1';
                } else if (i === index) {
                    thumb.style.order = '2';
                } else if (i === nextIndex) {
                    thumb.style.order = '3';
                }
            } else {
                thumb.style.display = 'none';
            }

            if (img) img.style.filter = 'grayscale(100%)';
            if (name) {
                name.style.color = '#ffab7d';
                name.style.fontWeight = '500';
            }
        });

        const activeTestimonial = testimonials[index];
        const activeThumb = thumbs[index];

        if (activeTestimonial && activeThumb) {
            activeTestimonial.style.display = 'block';
            setTimeout(() => {
                activeTestimonial.classList.add('active');
            }, 50);

            activeThumb.classList.add('active');
            const img = activeThumb.querySelector('.bio-image img');
            const name = activeThumb.querySelector('.bio-name');
            if (img) img.style.filter = 'none';
            if (name) {
                name.style.color = 'var(--accent)';
                name.style.fontWeight = '700';
            }
        }
        currentTestimonialIndex = index;
    }

    function startTestimonialAutoPlay() {
        clearInterval(testimonialInterval);
        testimonialInterval = setInterval(() => {
            if (!isTestimonialPaused) {
                let nextIndex = (currentTestimonialIndex + 1) % testimonials.length;
                showTestimonial(nextIndex);
            }
        }, 2500); // 2.5s timer
    }

    if (thumbs.length > 0 && testimonials.length > 0) {
        showTestimonial(0);
        startTestimonialAutoPlay();

        thumbs.forEach((thumb) => {
            thumb.addEventListener('click', () => {
                const index = parseInt(thumb.getAttribute('data-index'), 10);
                showTestimonial(index);
                startTestimonialAutoPlay();
            });
        });

        const testimonialContainer = document.querySelector('.testimonial-container');
        if (testimonialContainer) {
            testimonialContainer.addEventListener('mouseenter', () => {
                isTestimonialPaused = true;
            });
            testimonialContainer.addEventListener('mouseleave', () => {
                isTestimonialPaused = false;
            });
        }
    }

    // Global Certifications Slider Implementation
    const certTrack = document.querySelector('.certifications-track');
    const certSlides = document.querySelectorAll('.cert-slide');
    const certPrevBtn = document.querySelector('.cert-prev');
    const certNextBtn = document.querySelector('.cert-next');
    let certCurrentIndex = 0;
    let certInterval;

    function getVisibleSlidesCount() {
        if (window.innerWidth <= 575) return 1;
        if (window.innerWidth <= 991) return 2;
        return 3;
    }

    function updateCertSlider() {
        if (!certTrack || certSlides.length === 0) return;
        const visibleSlides = getVisibleSlidesCount();
        const maxIndex = certSlides.length - visibleSlides;
        
        if (certCurrentIndex > maxIndex) {
            certCurrentIndex = 0;
        } else if (certCurrentIndex < 0) {
            certCurrentIndex = maxIndex;
        }

        const slideWidth = certSlides[0].getBoundingClientRect().width;
        const gap = 30;
        const amountToMove = (slideWidth + gap) * certCurrentIndex;
        certTrack.style.transform = `translateX(-${amountToMove}px)`;
    }

    function nextCertSlide() {
        const visibleSlides = getVisibleSlidesCount();
        const maxIndex = certSlides.length - visibleSlides;
        if (certCurrentIndex >= maxIndex) {
            certCurrentIndex = 0;
        } else {
            certCurrentIndex++;
        }
        updateCertSlider();
    }

    function prevCertSlide() {
        const visibleSlides = getVisibleSlidesCount();
        const maxIndex = certSlides.length - visibleSlides;
        if (certCurrentIndex <= 0) {
            certCurrentIndex = maxIndex;
        } else {
            certCurrentIndex--;
        }
        updateCertSlider();
    }

    function startCertAutoPlay() {
        clearInterval(certInterval);
        certInterval = setInterval(nextCertSlide, 3000);
    }

    if (certTrack && certSlides.length > 0) {
        startCertAutoPlay();

        if (certNextBtn) {
            certNextBtn.addEventListener('click', () => {
                nextCertSlide();
                startCertAutoPlay();
            });
        }

        if (certPrevBtn) {
            certPrevBtn.addEventListener('click', () => {
                prevCertSlide();
                startCertAutoPlay();
            });
        }

        window.addEventListener('resize', () => {
            updateCertSlider();
        });
        
        setTimeout(updateCertSlider, 100);
    }

    // Intersection Observer for scroll animations (What We Offer cards)
    const offerCards = document.querySelectorAll('.service-card');
    if (offerCards.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const cardObserver = new IntersectionObserver((entries, observer) => {
            let delay = 0;
            // Filter entries that are actually intersecting
            const intersectingEntries = entries.filter(entry => entry.isIntersecting);
            
            intersectingEntries.forEach((entry) => {
                entry.target.style.transitionDelay = `${delay}ms`;
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
                delay += 100; // 100ms stagger between cards appearing together
            });
        }, observerOptions);

        offerCards.forEach((card) => {
            cardObserver.observe(card);
        });
    }

    // Intersection Observer for scroll animations (Why Choose Us cards)
    const chooseCards = document.querySelectorAll('.why-choose-card');
    if (chooseCards.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const chooseObserver = new IntersectionObserver((entries, observer) => {
            let delay = 0;
            const intersectingEntries = entries.filter(entry => entry.isIntersecting);
            
            intersectingEntries.forEach((entry) => {
                entry.target.style.transitionDelay = `${delay}ms`;
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
                delay += 100; // 100ms stagger between cards appearing together
            });
        }, observerOptions);

        chooseCards.forEach((card) => {
            chooseObserver.observe(card);
        });
    }

    // Intersection Observer for scroll animations (Expertise section)
    const expertiseSection = document.querySelector('.expertise-section');
    if (expertiseSection) {
        const expertiseImg = expertiseSection.querySelector('.expertise-image');
        const expertiseContent = expertiseSection.querySelector('.expertise-content');
        
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const expertiseObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    if (expertiseImg) expertiseImg.classList.add('revealed');
                    if (expertiseContent) expertiseContent.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        expertiseObserver.observe(expertiseSection);
    }

    // Intersection Observer for scroll animations (View All buttons)
    const viewAllButtons = document.querySelectorAll('.verify-btn');
    if (viewAllButtons.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const buttonObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        viewAllButtons.forEach((btn) => {
            buttonObserver.observe(btn);
        });
    }
});

