from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os

app = Flask(__name__)
app.secret_key = 'sortiq_clone_secret_key'

# Mock blog posts matching the original website insights
BLOG_POSTS = [
    {
        'id': 1,
        'title': 'How to Choose the Right Technology Stack for Your Website',
        'slug': 'how-to-choose-the-right-technology-stack-for-your-website',
        'date': 'April 30, 2026',
        'categories': ['Software Development', 'Web Development'],
        'summary': 'When Planning a Website, most people focus on design and features first...',
        'image': 'https://sortiqsolutions.com/wp-content/uploads/2026/04/How-to-Choose-the-Right-Technology-Stack-for-Your-Website.webp',
        'content': 'When Planning a Website, most people focus on design and features first. However, the technology stack you choose is the foundation of your website\'s performance, security, and scalability. A right tech stack ensures smooth operations and easier future upgrades.'
    },
    {
        'id': 2,
        'title': 'How a Fast Website Improves Google Ranking & User Experience',
        'slug': 'how-a-fast-website-improves-google-ranking-user-experience',
        'date': 'April 22, 2026',
        'categories': ['SEO', 'Web Development'],
        'summary': 'When someone visits your website, speed is the first thing they notice...',
        'image': 'https://sortiqsolutions.com/wp-content/uploads/2026/04/How-a-Fast-Website-Improves-Google-Ranking-and-User-Experience.webp',
        'content': 'When someone visits your website, speed is the first thing they notice. Google considers site speed as a critical ranking factor. Learn how optimizing loading speeds, images, and server responses translates to better SEO metrics and conversion rates.'
    },
    {
        'id': 3,
        'title': 'The Importance of UI/UX Design in Modern Web Development',
        'slug': 'the-importance-of-ui-ux-design-in-modern-web-development',
        'date': 'April 15, 2026',
        'categories': ['Web Designing', 'Web Development'],
        'summary': 'In today’s digital-first world, a website is more than just an online...',
        'image': 'https://sortiqsolutions.com/wp-content/uploads/2026/04/The-Importance-of-UIUX-Design-in-Modern-Web-Development.webp',
        'content': 'In today\'s digital-first world, a website is more than just an online brochure. It\'s an experience. Solid UI/UX design keeps users engaged, reduces bounce rates, and guides them effortlessly to your call-to-actions.'
    }
]

@app.route('/')
def index():
    return render_template('index.html', recent_posts=BLOG_POSTS)

@app.route('/about')
@app.route('/about-us/')
def about():
    return render_template('about.html')

@app.route('/why-choose-us/')
def why_choose_us():
    return render_template('about.html', tab='why-choose-us')

@app.route('/our-expertise/')
def our_expertise():
    return render_template('about.html', tab='our-expertise')

@app.route('/clients/')
def clients():
    return render_template('about.html', tab='clients')

@app.route('/our-career/')
def career():
    return render_template('about.html', tab='career')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/website-development-company/')
def web_development():
    return render_template('services/web_dev.html')

@app.route('/website-designing-company/')
def web_design():
    return render_template('services/web_design.html')

@app.route('/laravel-development-company/')
def laravel_development():
    return render_template('services/laravel.html')

@app.route('/wordpress-development-company/')
def wordpress_development():
    return render_template('services/wordpress.html')

@app.route('/ecommerce-development-company/')
def ecommerce_development():
    return render_template('services/ecommerce.html')

@app.route('/digital-marketing-company/')
def digital_marketing():
    return render_template('services/digital_marketing.html')

@app.route('/seo-company/')
def seo_company():
    return render_template('services/seo.html')

@app.route('/smo-company/')
def smo_company():
    return render_template('services/smo.html')

@app.route('/graphic-designing-company/')
def graphic_designing():
    return render_template('services/graphic.html')

@app.route('/banner-designing-company/')
def banner_designing():
    return render_template('services/banner.html')

@app.route('/logo-designing-company/')
def logo_designing():
    return render_template('services/logo.html')

@app.route('/website-maintenance/')
@app.route('/website-maintenance-company/')
def website_maintenance():
    return render_template('services/maintenance.html')

@app.route('/portfolios/')
def portfolios():
    return render_template('portfolio.html')

@app.route('/case-studies/')
def case_studies():
    return render_template('case_studies.html')

@app.route('/blog/')
def blog():
    return render_template('blog.html', posts=BLOG_POSTS)

@app.route('/blog/<slug>/')
def blog_detail(slug):
    post = next((p for p in BLOG_POSTS if p['slug'] == slug), None)
    if not post:
        return redirect(url_for('blog'))
    return render_template('blog_detail.html', post=post)

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/internship/')
def internship():
    return render_template('internship.html')

@app.route('/video/')
@app.route('/videos/')
def videos():
    return render_template('video.html')


# Form submissions
@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    data = request.form
    # In a real app, this would send an email or store in database
    return jsonify({'status': 'success', 'message': 'Thank you! Your enquiry has been received.'})

@app.route('/submit-fresher', methods=['POST'])
def submit_fresher():
    # Handle files
    cv_file = request.files.get('cv')
    # Save file or send email
    return jsonify({'status': 'success', 'message': 'Application submitted successfully.'})

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    # Handle message
    return jsonify({'status': 'success', 'message': 'Message sent successfully.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
