
// 导航栏滚动效果
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop) {
            // 向下滚动
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // 向上滚动
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
});

// 表单验证
const registerForm = document.querySelector('.register-form');
if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
        const name = document.getElementById('name').value;
        const studentId = document.getElementById('student_id').value;
        const className = document.getElementById('class_name').value;
        
        if (name.trim() === '') {
            e.preventDefault();
            showError('姓名不能为空');
            return;
        }

        if (studentId.trim() === '') {
            e.preventDefault();
            showError('学号不能为空');
            return;
        }

        if (className.trim() === '') {
            e.preventDefault();
            showError('班级不能为空');
            return;
        }
    });
}

// 错误提示函数
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error';
    errorDiv.textContent = message;
    
    const form = document.querySelector('.register-form');
    const formGroups = form.querySelectorAll('.form-group');
    form.insertBefore(errorDiv, formGroups[0]);

    // 3秒后移除错误提示
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

// 赛博朋克风格的光标效果
document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.createElement('div');
    cursor.className = 'cursor';
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    // 添加鼠标悬停效果
    const hoverElements = document.querySelectorAll('a, button, input, select');
    hoverElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            cursor.classList.add('cursor-hover');
        });
        element.addEventListener('mouseleave', () => {
            cursor.classList.remove('cursor-hover');
        });
    });
});

// 添加页面过渡效果
document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('fade-in');
});

// 添加滚动动画效果
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, {
        threshold: 0.1
    });

    animatedElements.forEach(element => {
        observer.observe(element);
    });
});

// 添加文字故障效果
document.addEventListener('DOMContentLoaded', () => {
    const glitchTexts = document.querySelectorAll('.glitch-text');
    
    glitchTexts.forEach(text => {
        const originalText = text.textContent;
        
        text.addEventListener('mouseenter', () => {
            let iterations = 0;
            const maxIterations = 10;
            
            const interval = setInterval(() => {
                text.textContent = originalText
                    .split('')
                    .map((char, index) => {
                        if (index < iterations) {
                            return originalText[index];
                        }
                        return String.fromCharCode(65 + Math.floor(Math.random() * 26));
                    })
                    .join('');
                
                iterations += 1/3;
                
                if (iterations >= maxIterations) {
                    clearInterval(interval);
                    text.textContent = originalText;
                }
            }, 30);
        });
    });
});

// 添加动态背景效果
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    canvas.className = 'background-canvas';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    // 调整画布大小
    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    // 创建粒子系统
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = Math.random() * 2 - 1;
            this.vy = Math.random() * 2 - 1;
            this.size = Math.random() * 2;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
        }

        draw() {
            ctx.fillStyle = '#0ff';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    const particles = Array.from({ length: 100 }, () => new Particle());

    function animate() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, width, height);

        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        requestAnimationFrame(animate);
    }

    animate();
});

// 添加表单输入动画效果
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('input-active');
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement.classList.remove('input-active');
            }
        });
    });
});
