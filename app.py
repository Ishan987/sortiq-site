from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_compress import Compress
import os

app = Flask(__name__)
Compress(app)
app.secret_key = 'sortiq_clone_secret_key'

import sqlite3
from werkzeug.utils import secure_filename
import json

DATABASE = os.path.join(app.root_path, 'sortiq.db')
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads', 'resumes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DEFAULT_SITE_LAYOUT = {
    "header": {
        "logo_text": "Sortiq Solutions",
        "phone": "+91 9646522110",
        "email": "info@sortiqsolutions.com",
        "apply_label": "Apply Internship",
        "apply_url": "/internship/"
    },
    "nav_links": [
        {"label": "Home", "url": "/", "has_dropdown": "0"},
        {"label": "About Us", "url": "/about-us/", "has_dropdown": "1"},
        {"label": "Services", "url": "/services/", "has_dropdown": "1"},
        {"label": "Our Work", "url": "/our-work/", "has_dropdown": "1"},
        {"label": "Blog", "url": "/blog/", "has_dropdown": "0"},
        {"label": "Contact Us", "url": "/contact/", "has_dropdown": "0"},
        {"label": "", "url": "", "has_dropdown": "0"},
        {"label": "", "url": "", "has_dropdown": "0"}
    ],
    "footer_badges": [
        {"label": "Goodfirms", "image": "/static/images/GF-min.png"},
        {"label": "Top Rated", "image": "/static/images/digital-marketing-logo-min.png"},
        {"label": "Upwork", "image": "/static/images/upwork-logo-min.png"},
        {"label": "Wix Partner", "image": "/static/images/EN_legend_small.png"},
        {"label": "ISO 9001", "image": "/static/images/iso-certified.webp"},
        {"label": "", "image": ""},
        {"label": "", "image": ""},
        {"label": "", "image": ""}
    ],
    "footer": {
        "address": "E-51, Second Floor, Phase - 8, Industrial Area, S.A.S. Nagar, Mohali, Punjab 160071",
        "phone": "+91 9646522110",
        "email": "sortiqsolutions@gmail.com",
        "certificate_text": "Verify your certificate's authenticity now.",
        "certificate_button_label": "Verify Now",
        "certificate_url": "https://erp.sortiqsolutions.com/certificate-verify",
        "chat_label": "Chat with us",
        "chat_url": "https://wa.me/+919646522110?text=Hello,%20I%20would%20like%20to%20know%20more%20about%20your%20services!"
    },
    "footer_columns": {
        "company": {
            "title": "Our Company",
            "links": [
                {"label": "Home", "url": "/"},
                {"label": "About Us", "url": "/about-us/"},
                {"label": "Why Choose Us", "url": "/why-choose-us/"},
                {"label": "Terms", "url": "/terms/"},
                {"label": "Portfolio", "url": "/portfolios/"},
                {"label": "Our Career", "url": "/our-career/"},
                {"label": "Our Clients", "url": "/clients/"},
                {"label": "Blog", "url": "/blog/"},
                {"label": "Contact Sortiq Solutions", "url": "/contact/"},
                {"label": "FAQ", "url": "/faq/"},
                {"label": "", "url": ""},
                {"label": "", "url": ""}
            ]
        },
        "services": {
            "title": "Our Services",
            "links": [
                {"label": "Web Designing", "url": "/website-designing-company/"},
                {"label": "Web Development", "url": "/website-development-company/"},
                {"label": "SEO", "url": "/seo-company/"},
                {"label": "SMO", "url": "/smo-company/"},
                {"label": "Digital Marketing", "url": "/digital-marketing-company/"},
                {"label": "eCommerce Development", "url": "/ecommerce-development-company/"},
                {"label": "App Development", "url": "/app-development-company/"},
                {"label": "Software Testing", "url": "/software-testing-company/"},
                {"label": "", "url": ""},
                {"label": "", "url": ""},
                {"label": "", "url": ""},
                {"label": "", "url": ""}
            ]
        },
        "solutions": {
            "title": "Solutions",
            "links": [
                {"label": "PHP Development", "url": "/php-development-company/"},
                {"label": "Laravel Development", "url": "/laravel-development-company/"},
                {"label": "CodeIgniter", "url": "/codeigniter-development-company/"},
                {"label": "Shopify Development", "url": "/shopify-development-company/"},
                {"label": "WordPress Development", "url": "/wordpress-development-company/"},
                {"label": "React JS Development", "url": "/react-js-development-company/"},
                {"label": "Node JS Development", "url": "/node-js-development-company/"},
                {"label": "Vue JS Development", "url": "/vue-js-development-company/"},
                {"label": "", "url": ""},
                {"label": "", "url": ""},
                {"label": "", "url": ""},
                {"label": "", "url": ""}
            ]
        }
    }
}

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fresher_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT,
            institute TEXT,
            technology TEXT,
            message TEXT,
            cv_filename TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT NOT NULL,
            date TEXT,
            categories TEXT,
            summary TEXT,
            image TEXT,
            content TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            platform TEXT,
            text TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT,
            title TEXT NOT NULL,
            technology TEXT,
            location TEXT,
            status TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            src TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS client_logos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pages_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT UNIQUE,
            title TEXT,
            description TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS site_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT
        )
    ''')
    conn.commit()
    
    cursor = conn.cursor()
    
    # Seed Blogs
    cursor.execute('SELECT COUNT(*) FROM blogs')
    if cursor.fetchone()[0] == 0:
        blogs_data = load_blogs()
        for blog in blogs_data:
            cats = ",".join(blog.get('categories', []))
            conn.execute(
                'INSERT INTO blogs (title, slug, date, categories, summary, image, content) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (blog['title'], blog['slug'], blog['date'], cats, blog.get('summary', ''), blog.get('image', ''), blog.get('content', ''))
            )
            
    # Seed Reviews
    cursor.execute('SELECT COUNT(*) FROM reviews')
    if cursor.fetchone()[0] == 0:
        reviews_data = load_reviews()
        for rev in reviews_data:
            conn.execute(
                'INSERT INTO reviews (author, platform, text) VALUES (?, ?, ?)',
                (rev['author'], rev.get('platform', 'Google'), rev['text'])
            )

    # Seed Portfolios
    cursor.execute('SELECT COUNT(*) FROM portfolios')
    if cursor.fetchone()[0] == 0:
        mock_projects = [
            ("#PRJ-092", "Zeitgeist Logistics Dashboard", "MERN Stack, Redis, AWS", "Munich, Germany", "Completed"),
            ("#PRJ-091", "Advantage Plus Tax Gateway", "React, Laravel, PostgreSQL", "Toronto, Canada", "Completed"),
            ("#PRJ-090", "Helium Recruiting Portal", "WordPress Custom API, PHP", "London, UK", "Completed"),
            ("#PRJ-089", "Kebaonish Brand E-commerce", "Shopify Plus, Liquid API", "Vancouver, Canada", "Completed"),
        ]
        for pcode, title, tech, loc, stat in mock_projects:
            conn.execute(
                'INSERT INTO portfolios (project_code, title, technology, location, status) VALUES (?, ?, ?, ?, ?)',
                (pcode, title, tech, loc, stat)
            )

    # Seed Videos
    cursor.execute('SELECT COUNT(*) FROM videos')
    if cursor.fetchone()[0] == 0:
        for pg, vids in VIDEOS_DATA.items():
            for vid in vids:
                conn.execute(
                    'INSERT INTO videos (title, src) VALUES (?, ?)',
                    (vid['title'], vid['src'])
                )

    # Seed Logos
    cursor.execute('SELECT COUNT(*) FROM client_logos')
    if cursor.fetchone()[0] == 0:
        for pg, logos in CLIENTS_DATA.items():
            for logo in logos:
                conn.execute(
                    'INSERT INTO client_logos (url) VALUES (?)',
                    (logo,)
                )

    # Seed Pages Metadata
    cursor.execute('SELECT COUNT(*) FROM pages_metadata')
    if cursor.fetchone()[0] == 0:
        pages_seed = [
            # COMPANY PAGES
            ('home', 'Sortiq Solutions - Smart Sorting IT Solutions', 'Professional software development, MERN, and SEO consulting agency.'),
            ('about', 'About Us - Sortiq Solutions', 'Learn more about our vision, core values, and dedicated team.'),
            ('why-choose-us', 'Why Choose Us - Sortiq Solutions', 'Understand what makes Sortiq Solutions a premium choice for web services.'),
            ('our-expertise', 'Our Technical Expertise - Sortiq Solutions', 'Discover the tech stacks, databases, and frameworks we specialize in.'),
            ('case-studies', 'Case Studies - Sortiq Solutions', 'Explore our success stories and portfolio case studies.'),
            ('our-career', 'Careers - Join Our Team | Sortiq Solutions', 'Explore job opportunities and internships at Sortiq Solutions.'),
            ('internship', 'Internship Program - Sortiq Solutions', 'Launch your career with our hands-on IT and software internship.'),
            ('faq', 'FAQ - Sortiq Solutions', 'Frequently asked questions about our software development and IT agency.'),
            ('support', 'Support - Sortiq Solutions', 'Get in touch with our helpdesk and customer support services.'),
            ('terms', 'Terms of Service - Sortiq Solutions', 'Read the terms and conditions governing the use of our services.'),
            ('contact', 'Contact Us - Sortiq Solutions', 'Reach out for inquiries, consultations, and custom IT project quotes.'),
            
            # CONTENT PAGES
            ('blog', 'Blog - Sortiq Solutions', 'Stay updated with our latest articles, insights, and tech tutorials.'),
            ('portfolio', 'Our Portfolio - Sortiq Solutions', 'Check out our showcased projects and design work.'),
            ('reviews', 'Client Reviews - Sortiq Solutions', 'Read what our clients say about our deliverables and services.'),
            ('clients', 'Our Clients - Sortiq Solutions', 'View our portfolio of satisfied clients and corporate partners.'),
            ('videos', 'Video Gallery - Sortiq Solutions', 'Watch our promotional material, walkthroughs, and visual portfolio.'),
            
            # SERVICE PAGES
            ('services-overview', 'Services Overview - Sortiq Solutions', 'Overview of all custom development, design, and marketing services.'),
            ('website-design', 'Website Designing Company - Sortiq Solutions', 'Custom UI/UX website designing services tailored for your brand.'),
            ('laravel', 'Laravel Development Services - Sortiq Solutions', 'Scalable, secure PHP applications built using the Laravel framework.'),
            ('wordpress', 'WordPress Development Services - Sortiq Solutions', 'Custom themes, plugins, and high-performance WordPress sites.'),
            ('ecommerce', 'E-commerce Development Services - Sortiq Solutions', 'Complete online stores, shopping carts, and secure payment integrations.'),
            ('digital-marketing', 'Digital Marketing Agency - Sortiq Solutions', 'Drive traffic, generate leads, and boost conversions with our digital plans.'),
            ('seo', 'SEO Consulting & Services - Sortiq Solutions', 'Rank higher on Google with our technical and on-page optimization services.'),
            ('smo', 'Social Media Optimization (SMO) - Sortiq Solutions', 'Optimize your brand presence across major social media networks.'),
            ('graphics', 'Graphic Designing Services - Sortiq Solutions', 'Professional layouts, illustrations, and digital branding assets.'),
            ('banners', 'Banner Designing Services - Sortiq Solutions', 'High-click-through promotional banners and display ads.'),
            ('logos', 'Logo Designing Services - Sortiq Solutions', 'Unique corporate logos and brand identity packages.'),
            ('maintenance', 'Website Maintenance Services - Sortiq Solutions', 'Regular backups, security patches, and performance optimizations.'),
            ('bigcommerce', 'BigCommerce Development Services - Sortiq Solutions', 'Enterprise-grade headless commerce and custom store setups.'),
            ('mern-stack', 'MERN Stack Development Services - Sortiq Solutions', 'Full-stack Javascript applications using MongoDB, Express, React, Node.js.'),
            ('app-development', 'Mobile App Development Services - Sortiq Solutions', 'Native and cross-platform apps built for iOS and Android devices.'),
            ('testing', 'Software Testing & Quality Assurance - Sortiq Solutions', 'Manual and automated testing to ensure bug-free software deployment.'),
            ('cyber-security', 'Cyber Security Services - Sortiq Solutions', 'Protect your infrastructure with our comprehensive security audits.'),
            ('hubspot', 'HubSpot Integration & Consulting - Sortiq Solutions', 'CRM setup, marketing automation, and HubSpot pipeline tuning.'),
            ('zoho', 'Zoho Consulting Services - Sortiq Solutions', 'Maximize efficiency with custom Zoho Creator and CRM solutions.'),
            ('php', 'Custom PHP Development Services - Sortiq Solutions', 'High-performance web applications built on core and framework PHP.'),
            ('codeigniter', 'CodeIgniter Development Services - Sortiq Solutions', 'Lightweight, rapid PHP web applications and API architectures.'),
            ('shopify', 'Shopify Development Services - Sortiq Solutions', 'Launch, optimize, and customize Shopify and Shopify Plus e-shops.'),
            ('react', 'ReactJS Frontend Development - Sortiq Solutions', 'Build snappy, dynamic single-page web applications with React.')
        ]
        for path, title, desc in pages_seed:
            conn.execute("INSERT OR IGNORE INTO pages_metadata (page_path, title, description) VALUES (?, ?, ?)", (path, title, desc))

    # Seed Site Settings
    cursor.execute('SELECT COUNT(*) FROM site_settings')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('phone', '+91 98889 00877')")
        conn.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('email', 'info@sortiqsolutions.com')")
        conn.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('address', 'IT Park, Block B, Chandigarh, India')")
        conn.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('site_layout', ?)", (json.dumps(DEFAULT_SITE_LAYOUT),))

    conn.commit()
    conn.close()

@app.after_request
def add_header(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

import json

def load_blogs():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM blogs ORDER BY id DESC').fetchall()
        conn.close()
        
        blogs_list = []
        for r in rows:
            b = dict(r)
            b['categories'] = [c.strip() for c in b['categories'].split(',')] if b['categories'] else []
            blogs_list.append(b)
        return blogs_list
    except Exception as e:
        print(f"Error loading blogs from database: {e}")
        json_path = os.path.join(app.root_path, 'static', 'blogs.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

def load_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Error loading reviews from database: {e}")
        json_path = os.path.join(app.root_path, 'static', 'reviews.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

@app.route('/')
def index():
    posts = load_blogs()
    # Show first 3 posts on homepage
    return render_template('index.html', recent_posts=posts[:3])

@app.route('/about')
@app.route('/about/')
@app.route('/about-us/')
def about():
    return render_template('about.html')

@app.route('/why-choose-us/')
def why_choose_us():
    return render_template('why_choose_us.html')

@app.route('/our-expertise/')
def our_expertise():
    return render_template('our_expertise.html')


# Client logos dataset
CLIENTS_DATA = {
    1: [
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/Perry.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/image.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/logo-header-dark-2023@2x.png.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/mbc-rev-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/zeitgeist-z.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/Think-Decks.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/ASSA_Logo_FC_Grad.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/Gold-Logo.jpg",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/Fuel-Kamloops-Logo.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/geigercars_logo.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/SoilOfHumility.png",
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/cropped-Advanatge-plus-tax-logo.png"
    ],
    2: [
        "https://sortiqsolutions.com/wp-content/uploads/2026/03/cropped-SW-LogoFinal-1.png",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/Kebaonish-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/helium-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/logo.png",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/Group-3@2x.png",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/cropped-Pinstripe-Logo-WHITE.jpg",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/advanatge-plus-tax-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/beachlander-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/dover-heights-community-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/royal-crest-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/wattman-logo.webp"
    ],
    3: [
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/coogee-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/bondi-business-women-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/Inspiration-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/korelife-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/koretraining-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/02/agentiiv-logo.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/cropped-PregnancyBirth_Parenting-1-450x110-1.png",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/cropped-cropped-floydglass_logo-1.png",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/cropped-hba-big-logo11-min.webp",
        "https://sortiqsolutions.com/wp-content/uploads/2025/01/cropped-thesitecoach_logo_final-2048x683-1.png"
    ]
}

@app.route('/clients/')
@app.route('/clients/page/<int:page>/')
def clients(page=1):
    if page not in CLIENTS_DATA:
        return redirect('/clients/')
    return render_template('clients.html', logos=CLIENTS_DATA[page], current_page=page)

@app.route('/our-career/')
def career():
    return render_template('our_career.html')

@app.route('/services')
def services():
    return render_template('services.html')



DYNAMIC_PAGES = {
    'terms': {
        'title': "Terms",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/11/GF-min.png",
        'intro_text': "By accessing and utilizing the web development, branding, and digital marketing services provided by Sortiq Solutions Pvt. Ltd., you agree to comply with our general standard terms of service.",
        'cards': [

        ]
    },
    'support': {
        'title': "Customer Support &amp; Help Center",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/11/GF-min.png",
        'intro_text': "“ We work systematically to integrated corporate responsibility in our corein business and make our expertise available for the benefit ”",
        'cards': [

        ]
    },
    'privacy-policy': {
        'title': "Privacy Policy - SortiqSoluitions",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/11/GF-min.png",
        'intro_text': "Welcome to Sortiq Solutions Pvt. Ltd. (“Company”, “we”, “our”, or “us”).\nWe are committed to protecting your privacy and ensuring that your personal information is handled in a safe and responsible manner.",
        'cards': [

        ]
    },
    'website-designing-company': {
        'title': "Best Website Designing Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/web-design-cover.webp",
        'intro_text': "Your website is not just an online presence it’s the first impression of your brand, a key trust builder, and a powerful sales tool. As a professional website designing company, Sortiq Solutions Pvt. Ltd. creates visually appealing, easy-to-use, and conversion-focused websites that clearly communicate your services. We design with your business goals in mind, helping you stand out online, engage visitors, and turn them into genuine leads and customers. We also ensure your website works seamlessly across all devices, loads fast, and is easy to manage as your business grows.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Custom Website Design:",
                'description': "We design unique, brand-aligned websites tailored to your business objectives. No templates - every layout, color, and interaction is designed to represent your brand identity."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "UI/UX Design",
                'description': "The user experience is the foundation of our designs. We prioritize user-friendly navigation,  clear content structure, and seamless interactions that naturally lead consumers to conversion"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Responsive & Mobile-First Design",
                'description': "Your website will look and perform flawlessly across all devices - desktops, tablets, and smartphones - ensuring a consistent experience for every user."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Landing Page Design",
                'description': "For advertisements, campaigns, and lead generation, we create high-converting landing pages that are designed for call-to-action effectiveness, speed, and clarity."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Website Redesign & Revamp",
                'description': "we revamp your existing website with a modern look, enhanced user experience, and increased engagement—all without sacrificing the core of your brand."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "CMS-Based Design",
                'description': "Using platforms like WordPress, Wix, Shopify, and Squarespace, we create user-friendly websites that give you complete control without requiring technical expertise."
            }
        ]
    },
    'website-development-company': {
        'title': "Best Laravel Development company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/web-development-cover.webp",
        'intro_text': "Sortiq Solutions Pvt. Ltd. is a trusted website development company helping businesses build a strong online presence. We create websites that connect with your target audience and support real business growth. Our focus is on clear layouts, thoughtful design, and smooth functionality so visitors can easily understand what you offer. Every website we create is fast, easy to use, and built to grow with your business helping you attract the right customers.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Custom Web Development",
                'description': "Our experts use cutting-edge technologies like node.js, Vue.js, Laravel, and PHP to create safe, responsive, and scalable solutions for both basic corporate websites and complex web applications.."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Content Management",
                'description': "From WordPress (custom themes, plugins, WooCommerce, migrations, performance tuning) to Shopify, Wix, or Squarespace, we create and optimize user-friendly, scalable websites."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "API Integration & Automation",
                'description': "Do you require marketing tools, payment gateways, analytics setup, or CRM integration? To optimize business efficiency and streamline processes, we integrate your website with third-party platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Performance Optimization",
                'description': "Your website will provide users with a dependable and seamless experience if it has quick loading times, optimized performance, clean code, and strong security measures"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Digital Marketing Ready",
                'description': "From a clean URL structure to page speed and mobile compatibility, our websites are designed with SEO best practices in mind to make sure you start on the right foot."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Ongoing Support",
                'description': "We provide continuous website support, regular updates, performance monitoring, and feature enhancements to ensure your website remains secure and   up to date."
            }
        ]
    },
    'seo-company': {
        'title': "#1 Best SEO Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/seo-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., our SEO services focus on long-term growth by improving how your website works and performs. We handle keyword usage, site structure, and technical fixes to ensure your website is easy for people to use and easy for search engines to understand. We start by understanding your business, your audience, and what success looks like for you. Based on that, we improve your website content, organize pages properly, and make sure important information is easy to find. This helps visitors stay longer and take action.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "SEO Strategy & Planning",
                'description': "We create specialized SEO strategies based on your business goals, market trends, and competitor analysis to ensure sustainable growth and improved rankings."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Keyword Research & Analysis",
                'description': "Our team conducts in-depth keyword research using high-intent and LSI keywords to target the most valuable search terms for your business and drive qualified traffic."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "On-Page SEO Optimization",
                'description': "We optimize website content, meta tags, headings, internal linking, and URL structure to improve relevance, user experience, and search engine visibility."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Technical SEO",
                'description': "From website speed optimization and mobile responsiveness to crawlability and indexation, we enhance the technical foundation of your site for better performance."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Local SEO Services",
                'description': "We optimize Google Business Profiles, local citations, location-based keywords, and reviews to increase visibility in local searches and drive traffic and inquiries."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Off-Page SEO",
                'description': "Our ethical link-building strategies help increase your domain authority, build trust with search engines, improve rankings, and strengthen your online presence."
            }
        ]
    },
    'smo-company': {
        'title': "Best SMO Company in Chandigarh Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/smo-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we blend data-driven strategies with creative storytelling to boost your visibility, engagement, and ROI across all major platforms. We keep things clear, focused, and aligned with your business goals. Our approach ensures consistent growth, measurable results, and long-term brand impact.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Social Profile Setup",
                'description': "We review and improve your profiles on platforms like Facebook, Instagram, LinkedIn, and Twitter to ensure your brand looks consistent, professional, and easy to understand."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Content That Feels Natural",
                'description': "We create posts, reels, graphics, and captions that fit each platform and speak to your audience in a natural way. No forced trends, just content that makes sense for your brand."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Managing Conversations",
                'description': "We help you stay connected with your audience by responding to comments and messages. This builds trust and shows people there’s a real team behind the brand."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Paid Ads (When Needed)",
                'description': "If advertising makes sense for your goals, we run focused ad campaigns to reach people who are more likely to be interested in your service and drive measurable results."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Honest Insights",
                'description': "You get clear updates on what’s working and what needs improvement. No confusing numbers, just useful insights to help you make better decisions."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Brand Consistency & Growth",
                'description': "We make sure your messaging, visuals, and tone stay consistent across all platforms. This helps strengthen your brand identity and supports steady, long-term growth."
            }
        ]
    },
    'digital-marketing-company': {
        'title': "Best Digital Marketing Company in Chadigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/digital-marketing-cover.webp",
        'intro_text': "Sortiq Solutions Pvt. Ltd. provides digital marketing services focused on real business growth. We help improve your online visibility, attract the right audience, and generate consistent leads. By combining smart planning, creative ideas, and clear data insights, we ensure your brand stands out and delivers measurable results even in competitive markets. From search engines to social media, we focus on practical actions that bring steady results, not short-term spikes. We help you build a strong and sustainable online presence.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Search Engine Optimization",
                'description': "We improve your search visibility with strategic SEO focused on keyword research, technical site optimization, and engaging content creation."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "PPC Advertising",
                'description': "We create & optimize Google Ads & paid media campaigns that efficiently target high-intent users, generate quality leads, and control ad budgets."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Social Media Marketing",
                'description': "Through social media content and paid ads, we help brands in increasing exposure and engagement and driving meaningful relationships."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Content Copywriting",
                'description': "From website copy to campaign content we create conversion-focused, SEO-friendly content to help you achieve your marketing goals."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Email Marketing",
                'description': "We create strategic, personalized email campaigns that engage your audience and drive conversions using data-driven insights."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Performance Tracking",
                'description': "We set up smart tracking and analytics to measure what matters, then optimize ads using user & conversion data for better results."
            }
        ]
    },
    'ecommerce-development-company': {
        'title': "Best ECommerce Development Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "Sortiq Solutions Pvt. Ltd. designs user-friendly, scalable, and secure eCommerce solutions tailored to your business goals. We focus on smooth user experiences, strong performance, and reliable security to help you attract customers, increase conversions, and grow your online store with confidence. From clear product layouts to fast loading pages and secure checkout processes, we make sure your online store supports real sales and long-term success.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Strategy",
                'description': "We analyze your business goals and audience to create a focused eCommerce strategy that drives engagement, conversions, and long-term growth."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Wireframing & Design",
                'description': "Our UI/UX designers create intuitive, user-friendly layouts that guide visitors smoothly from the home page to checkout. We focus on clear navigation and clean design."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Development",
                'description': "We build your store with clean code, secure payment setups, and mobile-first design so customers enjoy a smooth shopping experience on any device"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Testing & Quality Assurance",
                'description': "Every feature is rigorously tested for performance, speed, security, and usability before launch. We conduct cross-device and browser testing to ensure a smooth user experience."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Deployment & Launch",
                'description': "We deploy your website smoothly. The store goes live fully optimized, secure, and ready for users to browse, shop, and complete purchases without any issues."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Maintenance & Optimization",
                'description': "We continue improving your site after launch with regular updates, SEO enhancements, and performance tweaks to keep it running smoothly & up to date"
            }
        ]
    },
    'bigcommerce-development-company': {
        'title': "Best BigCommerce Development Company Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/shopify-cover.png",
        'intro_text': "Create a powerful BigCommerce online store designed for performance, usability, and growth.  BigCommerce development company, Sortiq Solutions Pvt. Ltd. design, develop, and optimize secure, scalable BigCommerce solutions that help brands grow faster, sell smarter, and deliver exceptional shopping experiences. From setting up products and payments to improving speed and usability, we create shopping experiences that are simple, trustworthy,  helping you sell confidently and scale with ease.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Business Understanding",
                'description': "To build a clear BigCommerce development plan, we understand your audience, product structure, goals, and technical needs."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Strategy & Planning",
                'description': "We design the store layout, features, integrations, and growth plans to ensure the BigCommerce solution scales with your needs."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Design & UX",
                'description': "We create a clean, conversion-focused BigCommerce design that delivers an intuitive user experience across all devices."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "BigCommerce Development",
                'description': "Using the best BigCommerce development techniques, our developers create unique themes, features, and integrations."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Testing & Optimization",
                'description': "We carefully check how well it works, how fast it responds, how safe it is, and if everything functions properly to make sure shopping is smooth."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch & Deployment",
                'description': "After final approval, we launch your BigCommerce store with proper configuration, security checks, and performance optimization."
            }
        ]
    },
    'mern-stack-development-company': {
        'title': "Best MERN Stack Development Company Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/mernstack-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we help businesses build web applications that are simple to use, dependable, and designed around real business needs. Before any development begins, we take time to understand your goals, your users, and how the application should support your everyday operations. Our MERN stack development approach focuses on clear communication, steady progress, and building solutions that can grow smoothly as your business evolves. We use modern technologies to create fast, responsive, and secure applications with clean architecture and scalable performance.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Understand Your Needs",
                'description': "We start by understanding your business, challenges, and expectations. This helps us stay aligned and avoid unnecessary work."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Plan with You",
                'description': "Together, we decide what features are needed and how the application should function. This keeps the project clear and avoids confusion."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Design for Ease of Use",
                'description': "We design the application so it feels simple and natural for users. Clear layouts and smooth flow help people get things done without frustration."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Build An Application",
                'description': "Using the MERN stack, we develop the application step by step. We keep everything organized so updates and changes are easier to manage."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Review Before Launch",
                'description': "We check the application to make sure it works properly and feels stable for everyday use. Any issues are addressed before going live."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch and Ongoing Support",
                'description': "We support you during launch and remain available afterward for updates, fixes, or improvements as your needs change."
            }
        ]
    },
    'app-development-company': {
        'title': "Best Mobile App Development Company Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "At Sortiq Solutions, we provide cutting-edge app development services to help businesses innovate and grow in the digital world. From intuitive UI/UX design to seamless functionality and performance optimization, our expert team builds custom mobile and web applications that deliver exceptional user experiences. Whether you’re launching a new app or enhancing an existing one, we’re here to turn your ideas into powerful, scalable solutions that drive business success.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Strategy",
                'description': "We begin by understanding your goals, target audience, and technical requirements to create a strategic plan for your website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Wireframing & Design",
                'description': "Our designers craft intuitive wireframes and stunning visual designs that enhance user experience and align with your brand identity."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Development & Coding",
                'description': "Using the latest technologies, our developers transform designs into a fully functional, responsive, and scalable website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Testing & Quality Assurance",
                'description': "We conduct rigorous testing to ensure your website performs flawlessly across all devices, browsers, and platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Deployment & Launch",
                'description': "Once everything is optimized and approved, we deploy your website with a smooth, hassle-free launch process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Maintenance & Optimization",
                'description': "We provide ongoing support, updates, and SEO enhancements to ensure your website remains fast, secure, and up to date."
            }
        ]
    },
    'software-testing-company': {
        'title': "Top Software Testing Company in Chandigarh Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/software-testing-cover.webp",
        'intro_text': "As a trusted software testing company, Sortiq Solutions Pvt. Ltd. provides complete software testing services to make sure your applications work as they should. We carefully check for errors, performance issues, and usability problems so your software runs smoothly and remains secure. By using both manual and automated testing methods, we help improve quality, reduce risks, and ensure your users enjoy a reliable and positive experience every time. The result is a stable, dependable product that you can confidently launch, maintain, and scale.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Requirement Analysis",
                'description': "We review your business needs, user expectations, and application functionality to understand what needs testing and define standards."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Test Planning",
                'description': "A clear test plan outlines the testing scope, tools, timelines, environments, and resources, aligned with your process to ensure smooth execution."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Test Case & Scenario Design",
                'description': "Test cases and scenarios are created in detail to check every feature, workflow, and possible edge case, ensuring complete test coverage."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Test Execution",
                'description': "Our expert team executes manual and automated tests across devices to identify functional, UI, performance, and compatibility issues."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Defect Reporting & Tracking",
                'description': "All identified issues are documented with clear steps, severity levels, and screenshots, and continuously tracked until they are resolved."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Re-Testing & Final Validation",
                'description': "Once fixes are applied, we re-test affected areas, perform regression testing to ensure stability, and deliver a quality-assured product."
            }
        ]
    },
    'website-maintenance-company': {
        'title': "Best Website Maintenance Company In Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/website-maintenance-cover.webp",
        'intro_text': "With Sortiq Solutions Pvt. Ltd., your website stays secure, updated, and performing at its best. As a trusted website maintenance company, we take care of regular updates, security monitoring, performance improvements, backups, and ongoing support allowing you to focus on growing your business without worry. Whether it’s a small update or ongoing care, we provide steady support so your website continues to support your business without interruptions or stress.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Initial Audit & Goal Setting",
                'description': "We start by evaluating your website’s performance, security status, and business objectives. This allows us to create a fully customized maintenance plan for long-term success."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Backup & Security Setup",
                'description': "To protect your data, we set up regular backups and continuous security checks. This ensures your website is safe from threats and can be quickly restored if any issue arises."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Software & Content Updates",
                'description': "As a professional website maintenance company, we keep your CMS, plugins, themes, and content up to date to maintain compatibility, security, and a fresh user experience."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Performance Optimization",
                'description': "By optimizing load times, resolving technical problems, and ensuring seamless operation across all devices and browsers, we improve the speed and stability of websites."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Functionality Testing",
                'description': "Your website is regularly tested to ensure all features, including forms, navigation, and interactive elements, work properly without errors or disruptions at all times."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Ongoing Support & Reporting",
                'description': "You receive clear updates on completed maintenance tasks, along with ongoing support to resolve issues and recommend improvements as your website evolves."
            }
        ]
    },
    'cyber-security-development': {
        'title': "Cyber Security Development Services",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., you get cyber security development solutions that protect your digital assets, strengthen your security defenses, and build trust with your customers. From secure architecture planning to proactive threat mitigation, we help you embed strong security across every layer of your digital ecosystem. Our approach is practical and preventive, helping you avoid issues before they cause disruption. We ensure your systems remain protected as your business grows so your business can operate with confidence and peace of mind.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Security Requirement",
                'description': "We start by analyzing your infrastructure and business goals to define cybersecurity objectives that protect your systems effectively."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Secure Architecture & Design",
                'description': "Our experts create secure system setups that reduce chances of attack and build security features from the start of the development process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Threat & Vulnerability",
                'description': "We simulate attack scenarios and analyze weak points in your applications and networks to identify risks before they become breaches."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Security Implementation",
                'description': "We use safe coding methods to create and improve systems that protect against cyber attacks using access limits and encryption."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Security Testing & Penetration",
                'description': "Through testing, including penetration testing, ethical hacking, and code reviews, we assess security strength and identify vulnerabilities."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Monitoring & Maintenance",
                'description': "After deployment, we provide monitoring, patches, and incident response to ensure security and quick recovery from threats."
            }
        ]
    },
    'hubspot-crm-services': {
        'title': "Best Laravel Development company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/laravel-development-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we provide expert HubSpot CRM services to streamline operations, manage contacts, and improve communication. Our team customizes the CRM setup and integrations to fit your business, helping increase productivity, manage leads effectively, and make smarter decisions with real-time insights.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "HubSpot CRM Setup",
                'description': "We set up HubSpot CRM to help businesses manage contacts, deals, and customer information efficiently, keeping everything organized in one system."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Contact & Lead Management",
                'description': "We organize customer data in HubSpot CRM, making it simple to track leads, manage contacts, and monitor client interactions in one place."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Sales Pipeline Management",
                'description': "We build a clear sales pipeline in HubSpot CRM to track deals, manage opportunities, and see exactly where each prospect is in the process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Marketing Automation",
                'description': "We automate marketing tasks in HubSpot CRM, including emails, lead nurturing, and follow-ups, so your team can focus on business growth"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Integration With Other Tools",
                'description': "We connect HubSpot CRM with your website, email platforms, and other tools for smooth data flow and efficient workflow management."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Reporting & Analytics",
                'description': "We create dashboards and reports in HubSpot CRM to monitor sales, marketing, and customer engagement for better business decisions"
            }
        ]
    },
    'zoho-crm-services': {
        'title': "Best Laravel Development company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/laravel-development-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we simplify customer management with Zoho CRM. We help businesses organize leads, track sales, and communicate better. Our team sets up and customizes Zoho CRM to fit your needs, so you can manage contacts, automate tasks, and gain clear insights to work efficiently and grow faster.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Business Requirement Analysis",
                'description': "We study your business processes, sales workflows, and customer needs to design a Zoho CRM setup that fits your goals perfectly."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "CRM Planning & Setup",
                'description': "We configure Zoho CRM with modules, fields, pipelines, and dashboards to manage leads, contacts, and sales efficiently."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Customization & Automation",
                'description': "We tailor Zoho CRM to your workflows, adding automation like lead assignment, task reminders, and workflow rules to save time."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Integration with Tools",
                'description': "We connect Zoho CRM to your website, email, marketing tools, and other apps to ensure smooth data flow and seamless communication."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Testing & Optimization",
                'description': "We thoroughly test and optimize the CRM setup, ensuring workflows, reports, and dashboards track performance accurately."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Training & Support",
                'description': "We provide training and ongoing support to help your team use Zoho CRM effectively and implement updates as your business grows."
            }
        ]
    },
    'php-development-company': {
        'title': "Best PHP Web Development Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/php-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., a trusted PHP development company, we build PHP applications that are stable, secure, and easy to manage. Our focus is simple: understand what your business actually needs and build solutions that work today and can grow tomorrow. From websites to custom backend systems and API integrations, we create solutions that are clean, well-structured, and easy to maintain. We communicate clearly and deliver solutions that simplify your workflow and support your long-term goals. Partner with us to turn your ideas into scalable digital success.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Understanding Your Vision",
                'description': "Before writing any code, we listen. We understand your business goals, users, and challenges. This helps us suggest the right PHP solution."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Planning the Structure",
                'description': "We plan the application flow, database, and user experience to keep everything clean, scalable, and easy to use for users and your team."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Secure PHP Development",
                'description': "As a PHP Development Company, we follow best practices to write clean, secure code using reliable frameworks to avoid issues."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "API Integrations",
                'description': "Need payment gateways, CRMs, or external tools? We integrate only what fits your workflow and ensure everything works smoothly together."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Testing Before Launch",
                'description': "We test the application for performance, security, and compatibility to ensure a stable experience after launch."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch & Ongoing Support",
                'description': "Once the project goes live, we stay available. We help with updates, fixes, and improvements so your PHP application continues to run smoothly."
            }
        ]
    },
    'laravel-development-company': {
        'title': "Best Laravel Development company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/laravel-development-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we help you build Laravel applications that support your day-to-day business needs. We start by understanding what you want to achieve, ask clear questions, and then develop a solution that fits your goals without adding features you don’t need or using confusing terms. As a trusted Laravel development company, we deliver scalable, secure solutions tailored to your business. Partner with us to transform your ideas into powerful digital solutions.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Understand Your Goals",
                'description': "We begin with a conversation. We ask questions to understand your idea, your users, and what you want to achieve. This helps us stay focused and avoid assumptions from day one."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Plan the Right Approach",
                'description': "Once your goals are clear, we plan how the application should work. This includes features, user flow, and basic structure so everyone knows what’s being built and why."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Test Before Going Live",
                'description': "Before launch, we carefully test the application to make sure everything works as expected. This helps reduce issues after launch and gives you confidence in the final result."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Design with Users in Mind",
                'description': "We design screens that feel natural and simple. The focus is always on clarity and usability so users can find what they need and get things done without confusion."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Build with Laravel",
                'description': "We use Laravel to develop the application step by step. We keep the code clean and organized so future updates are easier, more cost-effective, and hassle-free."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch & Ongoing Support",
                'description': "We help you launch smoothly and stay available afterward. Whether it’s small fixes, updates, or improvements, we support you as your needs evolve."
            }
        ]
    },
    'codeigniter-development-company': {
        'title': "Best CodeIgniter Development Company Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/codeIgniter-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we are a reliable codeIgniter development company delivering fast, secure, and scalable web applications tailored to your business needs. Using the lightweight CodeIgniter framework, our expert team builds robust solutions with clean architecture and smooth performance. Let us help you build robust web solutions with the efficiency of CodeIgniter. Our focus is on simple design, reliable performance, and long-term usability so you get a web solution that supports your business.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Expert CodeIgniter Developers",
                'description': "Our skilled developers have strong knowledge in creating fast and effective CodeIgniter applications that fit different business requirements."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Reliable Support & Maintenance",
                'description': "To keep your application  running smoothly, our staff offers updates, performance optimization, and ongoing support."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Secure & Scalable Development",
                'description': "Every application is built with strong security standards and a flexible structure that allows your business to expand easily over time."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Clean & Maintainable Code",
                'description': "We use standard coding methods to build clear, well-structured applications that are easy to manage, update, and scale with your business."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Transparent Process",
                'description': "You receive clear timelines, regular updates on how things are going, and open communication throughout the entire development process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Business-Focused Solutions",
                'description': "We focus on understanding your goals and providing solutions that add real value and support your long-term business growth."
            }
        ]
    },
    'shopify-development-company': {
        'title': "Shopify Development Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/shopify-cover.png",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we help you create and improve Shopify stores in a clear and effective way. We take time to understand your products, your customers, and your sales plan, and then build a store that fits your needs perfectly. As a trusted Shopify development company, we deliver solutions that are user-friendly, scalable, and designed to boost your sales. Build a Shopify store that drives sales and loyalty",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "First Conversation",
                'description': "We start by understanding your business and your goals for the store. This helps us focus on what matters and plan the work properly."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Check Before Launch",
                'description': "Before going live, we test the store to make sure links, checkout, and basic functions work properly on different devices."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Launch & Support",
                'description': "We help you launch smoothly and stay available if you need help later—for fixes, updates, or small improvements."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Decide What’s Needed",
                'description': "Together, we decide what pages, features, and settings your store actually needs. This keeps the work focused and avoids unnecessary changes later."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Design the Store",
                'description': "We design the store so customers can browse easily, understand your products, and complete purchases without confusion. The layout stays clean and clear."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Build the Store",
                'description': "We set up your Shopify store, add products, and configure payments and basic settings. Everything is arranged so you can manage it comfortably after launch."
            }
        ]
    },
    'wordpress-development-company': {
        'title': "Best Wordpress Development Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wordpress-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we design WordPress websites that are easy to use and easy to manage. We take time to understand what you need, explain things clearly, and build a website that supports your business without adding stress. No technical overload. No unnecessary features. Just a website that works. Built to grow with your business and deliver a smooth experience for your users. Empower your brand online with a WordPress site that truly makes an impact.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "We Start by Listening",
                'description': "​We begin with a simple conversation. We ask about your business, your customers, and what you want your website to do. This helps us stay clear and avoid assumptions."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Design for Real People",
                'description': "​We design your website so visitors can easily find what they’re looking for. Clean layouts, clear sections, and simple navigation are nothing complicated."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Build the Website",
                'description': "​We set up your WordPress site step by step and make sure everything works properly. The site is built so you can update content later without needing help every time."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Plan What’s Needed",
                'description': "​Before building anything, we agree on what pages and features are required. This keeps the process smooth and avoids last-minute confusion."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Check Before Going Live",
                'description': "​We test the website on different screens and devices to make sure pages load well and forms work as expected."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch & Ongoing Help",
                'description': "​Once the site is live, we will be available for support, updates, and small improvements as your needs change."
            }
        ]
    },
    'react-js-development-company': {
        'title': "Best React JS Development Company in Chandigarh Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/react-development-cover.webp",
        'intro_text': "When you choose Sortiq Solutions Pvt. Ltd., you partner with a reliable React JS development company that helps turn your ideas into fast, interactive, and scalable web applications. Our team of experts uses React JS to create high-performance, visually appealing interfaces that offer smooth user experiences and help your business grow. Our team focuses on clean design, quick loading, and flexible applications that can grow with your business. The goal is to create easy interfaces that support your long-term business needs.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Requirement",
                'description': "We start by understanding your business goals, target users, and project expectations. This ensures that your React application has a well-defined roadmap and goals."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Design & Architecture",
                'description': "Your application is designed with user experience in mind. We create user-friendly UI designs and a scalable architecture that supports performance and flexibility."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Testing & Quality Assurance",
                'description': "Before launch, your application goes through detailed testing to ensure stability, security, performance, and full compatibility across all devices and browsers."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "React JS Development & Coding",
                'description': "Our developers create clean, modular, and reusable React components using best practices. This leads to responsive, quick-loading apps that provide smooth interactions."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "API Integration & Backend Connectivity",
                'description': "We enable smooth data flow, authentication, payments, and other critical features by integrating your React application with secure backend systems and APIs."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Deployment & Ongoing Support",
                'description': "After your application has been authorized, we deploy it to the live environment and offer ongoing maintenance, updates, and support to keep it functioning properly."
            }
        ]
    },
    'node-js-development-company': {
        'title': "Best Custom Node.js Development Company",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we build Node.js applications that support real business needs. Our focus is on understanding your requirements, then developing systems that are reliable, easy to manage, and suited to your long-term goals. We communicate clearly and keep the process easy. As a trusted Node Js development company, we deliver scalable, secure solutions and ensures your applications are built to grow with your business.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Strategy",
                'description': "We begin by understanding your goals, target audience, and technical requirements to create a strategic plan for your website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Wireframing & Design",
                'description': "Our designers craft intuitive wireframes and stunning visual designs that enhance user experience and align with your brand identity."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Development & Coding",
                'description': "Using the latest technologies, our developers transform designs into a fully functional, responsive, and scalable website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Testing & Quality Assurance",
                'description': "We conduct rigorous testing to ensure your website performs flawlessly across all devices, browsers, and platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Deployment & Launch",
                'description': "Once everything is optimized and approved, we deploy your website with a smooth, hassle-free launch process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Maintenance & Optimization",
                'description': "We provide ongoing support, updates, and SEO enhancements to ensure your website remains fast, secure, and up to date."
            }
        ]
    },
    'vue-js-development-company': {
        'title': "Vue JS Development Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we build Vue.js applications that are easy to use, stable, and tailored to your business needs. We take time to understand what you need first, then plan and build clean solutions that help your team and users stay productive. As a trusted Vue Js development company, we focus on creating secure, scalable and high-performance applications whether it’s dynamic front-end interfaces or API integrations. Take your digital journey forward with confidence.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Strategy",
                'description': "We begin by understanding your goals, target audience, and technical requirements to create a strategic plan for your website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Wireframing & Design",
                'description': "Our designers craft intuitive wireframes and stunning visual designs that enhance user experience and align with your brand identity."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Development & Coding",
                'description': "Using the latest technologies, our developers transform designs into a fully functional, responsive, and scalable website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Testing & Quality Assurance",
                'description': "We conduct rigorous testing to ensure your website performs flawlessly across all devices, browsers, and platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Deployment & Launch",
                'description': "Once everything is optimized and approved, we deploy your website with a smooth, hassle-free launch process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Maintenance & Optimization",
                'description': "We provide ongoing support, updates, and SEO enhancements to ensure your website remains fast, secure, and up to date."
            }
        ]
    },
    'graphic-designing-company': {
        'title': "Best Graphic Designing Company in Chandigarh &amp; Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/graphic-design-cover.webp",
        'intro_text': "We help bring your ideas to life through clear and thoughtful design that reflects your business. From logos to marketing materials, Sortiq Solutions Pvt. Ltd. creates custom designs that look professional, connect with your audience, and support your business goals. We focus on understanding your brand, keeping things simple, and delivering designs that work across digital and print platforms. We create designs that enhance your brand and make an impact, whether they be for your website, social media, or offline marketing. We ensure the final design matches your vision and audience.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Logo & Brand Identity",
                'description': "We design unique and memorable logos along with clear brand guidelines that help your business look consistent."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Promotional & Social Visuals",
                'description': "Create eye-catching flyers, brochures, and social media visuals that grab attention, communicate clearly, and encourage people to engage."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Print & Packaging Design",
                'description': "High-quality designs for business cards and product packaging that help your brand stand out, look professional, and stay memorable."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Visual Stories & Infographics",
                'description': "Turning complex information into simple, clear visuals that are easy to understand and remember, while helping your message stand out."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Video & Motion Content",
                'description': "Dynamic animated logos, promotional video, and motion elements that bring your brand to life and increase engagement across digital platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Banner & Display Ad Design",
                'description': "Simple and eye-catching designs for online ads that grab attention and clearly share your message across digital platforms."
            }
        ]
    },
    'logo-designing-company': {
        'title': "Best Logo Designing Company in Chandigarh Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/logo-design-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we design unique, scalable, and memorable logos that truly represent your brand. We take time to understand your business, values, and audience, so your logo feels right, works seamlessly across all platforms, and leaves a strong, lasting impression. Our designs are clean, flexible, and easy to use across websites, social media, and print. The goal is to give you a logo that looks professional, builds trust, and leaves a strong, lasting impression wherever your brand appears.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Brand Research",
                'description': "We begin by understanding your brand, industry, and audience to create a logo that aligns with your goals and makes a strong first impression"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Concept Ideation",
                'description': "Our team creates multiple original logo concepts based on your brand strategy, focusing on creativity and relevance to make your brand stand out."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Design Refinement",
                'description': "After you choose a concept, we refine it with your feedback adjusting colors, typography, and shapes until the logo perfectly reflects your brand."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Finalization",
                'description': "Once approved, we deliver your logo in all key formats (AI, SVG, PNG, JPEG), optimized for web, social media, print, and branding to ensure consistent visibility."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Brand Style Guide",
                'description': "We provide guidance on proper logos, use spacing, colors, and backgrounds  to maintain consistency and keep your brand looking professional."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Post-Delivery Support",
                'description': "Our support continues after delivery, helping with updates, resizing, or format changes so your logo stays adaptable as your business grows across different platforms."
            }
        ]
    },
    'banner-designing-company': {
        'title': "Best Banner Designing Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/banner-design-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we create high-quality, eye-catching banners for digital and print platforms. From websites and social media to digital ads and events, our designs help elevate your brand and engage your audience effectively. Our focus is on simple layouts, readable text, and visuals that guide viewers toward action. The result is banner designs that not only look good but also support your marketing efforts, strengthen brand recall, and contribute to real business outcomes.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Requirement Analysis",
                'description': "Our process begins with understanding your brand, campaign objectives, audience preferences, and technical requirements."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Creative Concept Development",
                'description': "Once we have gathered your requirements, our creative team brainstorms and develops banner concepts tailored to your goals."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Design Drafting & Mockups Pro",
                'description': "Next, we create banner drafts and mockups that align with your campaign vision, brand goals, and overall visual direction."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Review, Feedback & Refinement",
                'description': "After presenting initial designs, we collaborate with you to refine the banner, adjusting colors, text, and visuals to meet your expectations."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Finalization & Exporting Files Process",
                'description': "Once approved, we finalize your banner design and prepare all necessary file formats optimized for web, social media, and print use."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Delivery & Ongoing Support Services",
                'description': "As a reliable banner designing company, we don’t just hand over files, we also provide guidance on best usage practices."
            }
        ]
    },
    'data-science-development': {
        'title': "Data Science Development Services",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we help you make better use of your data in ways that truly support your business. We begin by understanding what you want to achieve, then turn your data into clear insights you can actually use. As a trusted Vue.js development company, we build secure and fast applications that grow with your business. Whether you’re looking to identify trends, plan more effectively, or keep your data well organized, our focus is on practical results so using your data never feels confusing. We keep everything straightforward, so working with your data always feels simple",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Discovery & Strategy",
                'description': "We begin by understanding your goals, target audience, and technical requirements to create a strategic plan for your website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Wireframing & Design",
                'description': "Our designers craft intuitive wireframes and stunning visual designs that enhance user experience and align with your brand identity."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Development & Coding",
                'description': "Using the latest technologies, our developers transform designs into a fully functional, responsive, and scalable website."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Testing & Quality Assurance",
                'description': "We conduct rigorous testing to ensure your website performs flawlessly across all devices, browsers, and platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Deployment & Launch",
                'description': "Once everything is optimized and approved, we deploy your website with a smooth, hassle-free launch process."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Maintenance & Optimization",
                'description': "We provide ongoing support, updates, and SEO enhancements to ensure your website remains fast, secure, and up to date."
            }
        ]
    },
    'website-development': {
        'title': "Best Laravel Development company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/web-development-cover.webp",
        'intro_text': "Sortiq Solutions Pvt. Ltd. is a trusted website development company helping businesses build a strong online presence. We create websites that connect with your target audience and support real business growth. Our focus is on clear layouts, thoughtful design, and smooth functionality so visitors can easily understand what you offer. Every website we create is fast, easy to use, and built to grow with your business helping you attract the right customers.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Custom Web Development",
                'description': "Our experts use cutting-edge technologies like node.js, Vue.js, Laravel, and PHP to create safe, responsive, and scalable solutions for both basic corporate websites and complex web applications.."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Content Management",
                'description': "From WordPress (custom themes, plugins, WooCommerce, migrations, performance tuning) to Shopify, Wix, or Squarespace, we create and optimize user-friendly, scalable websites."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "API Integration & Automation",
                'description': "Do you require marketing tools, payment gateways, analytics setup, or CRM integration? To optimize business efficiency and streamline processes, we integrate your website with third-party platforms."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Performance Optimization",
                'description': "Your website will provide users with a dependable and seamless experience if it has quick loading times, optimized performance, clean code, and strong security measures"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Digital Marketing Ready",
                'description': "From a clean URL structure to page speed and mobile compatibility, our websites are designed with SEO best practices in mind to make sure you start on the right foot."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Ongoing Support",
                'description': "We provide continuous website support, regular updates, performance monitoring, and feature enhancements to ensure your website remains secure and   up to date."
            }
        ]
    },
    'graphic-design': {
        'title': "Best Graphic Designing Company in Chandigarh &amp; Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/graphic-design-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we design unique, scalable, and memorable logos that truly represent your brand. We take time to understand your business, values, and audience, so your logo feels right, works seamlessly across all platforms, and leaves a strong, lasting impression. Our designs are clean, flexible, and easy to use across websites, social media, and print. The goal is to give you a logo that looks professional, builds trust, and leaves a strong, lasting impression wherever your brand appears.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Brand Research",
                'description': "We begin by understanding your brand, industry, and audience to create a logo that aligns with your goals and makes a strong first impression"
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Concept Ideation",
                'description': "Our team creates multiple original logo concepts based on your brand strategy, focusing on creativity and relevance to make your brand stand out."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Design Refinement",
                'description': "After you choose a concept, we refine it with your feedback adjusting colors, typography, and shapes until the logo perfectly reflects your brand."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Finalization",
                'description': "Once approved, we deliver your logo in all key formats (AI, SVG, PNG, JPEG), optimized for web, social media, print, and branding to ensure consistent visibility."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Brand Style Guide",
                'description': "We provide guidance on proper logos, use spacing, colors, and backgrounds  to maintain consistency and keep your brand looking professional."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Post-Delivery Support",
                'description': "Our support continues after delivery, helping with updates, resizing, or format changes so your logo stays adaptable as your business grows across different platforms."
            }
        ]
    },
    'digital-marketing': {
        'title': "Best Digital Marketing Company in Chadigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/digital-marketing-cover.webp",
        'intro_text': "Sortiq Solutions Pvt. Ltd. provides digital marketing services focused on real business growth. We help improve your online visibility, attract the right audience, and generate consistent leads. By combining smart planning, creative ideas, and clear data insights, we ensure your brand stands out and delivers measurable results even in competitive markets. From search engines to social media, we focus on practical actions that bring steady results, not short-term spikes. We help you build a strong and sustainable online presence.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Search Engine Optimization",
                'description': "We improve your search visibility with strategic SEO focused on keyword research, technical site optimization, and engaging content creation."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "PPC Advertising",
                'description': "We create & optimize Google Ads & paid media campaigns that efficiently target high-intent users, generate quality leads, and control ad budgets."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Social Media Marketing",
                'description': "Through social media content and paid ads, we help brands in increasing exposure and engagement and driving meaningful relationships."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Content Copywriting",
                'description': "From website copy to campaign content we create conversion-focused, SEO-friendly content to help you achieve your marketing goals."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Email Marketing",
                'description': "We create strategic, personalized email campaigns that engage your audience and drive conversions using data-driven insights."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Performance Tracking",
                'description': "We set up smart tracking and analytics to measure what matters, then optimize ads using user & conversion data for better results."
            }
        ]
    },
    'laravel-development': {
        'title': "Best Laravel Development company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/laravel-development-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we help you build Laravel applications that support your day-to-day business needs. We start by understanding what you want to achieve, ask clear questions, and then develop a solution that fits your goals without adding features you don’t need or using confusing terms. As a trusted Laravel development company, we deliver scalable, secure solutions tailored to your business. Partner with us to transform your ideas into powerful digital solutions.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Understand Your Goals",
                'description': "We begin with a conversation. We ask questions to understand your idea, your users, and what you want to achieve. This helps us stay focused and avoid assumptions from day one."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Plan the Right Approach",
                'description': "Once your goals are clear, we plan how the application should work. This includes features, user flow, and basic structure so everyone knows what’s being built and why."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Test Before Going Live",
                'description': "Before launch, we carefully test the application to make sure everything works as expected. This helps reduce issues after launch and gives you confidence in the final result."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Design with Users in Mind",
                'description': "We design screens that feel natural and simple. The focus is always on clarity and usability so users can find what they need and get things done without confusion."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Build with Laravel",
                'description': "We use Laravel to develop the application step by step. We keep the code clean and organized so future updates are easier, more cost-effective, and hassle-free."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch & Ongoing Support",
                'description': "We help you launch smoothly and stay available afterward. Whether it’s small fixes, updates, or improvements, we support you as your needs evolve."
            }
        ]
    },
    'wordpress-development': {
        'title': "Best Wordpress Development Company in Chandigarh",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wordpress-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we design WordPress websites that are easy to use and easy to manage. We take time to understand what you need, explain things clearly, and build a website that supports your business without adding stress. No technical overload. No unnecessary features. Just a website that works. Built to grow with your business and deliver a smooth experience for your users. Empower your brand online with a WordPress site that truly makes an impact.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "We Start by Listening",
                'description': "​We begin with a simple conversation. We ask about your business, your customers, and what you want your website to do. This helps us stay clear and avoid assumptions."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Design for Real People",
                'description': "​We design your website so visitors can easily find what they’re looking for. Clean layouts, clear sections, and simple navigation are nothing complicated."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Build the Website",
                'description': "​We set up your WordPress site step by step and make sure everything works properly. The site is built so you can update content later without needing help every time."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Plan What’s Needed",
                'description': "​Before building anything, we agree on what pages and features are required. This keeps the process smooth and avoids last-minute confusion."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Check Before Going Live",
                'description': "​We test the website on different screens and devices to make sure pages load well and forms work as expected."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch & Ongoing Help",
                'description': "​Once the site is live, we will be available for support, updates, and small improvements as your needs change."
            }
        ]
    },
    'mern-stack': {
        'title': "Best MERN Stack Development Company Mohali",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/mernstack-cover.webp",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we help businesses build web applications that are simple to use, dependable, and designed around real business needs. Before any development begins, we take time to understand your goals, your users, and how the application should support your everyday operations. Our MERN stack development approach focuses on clear communication, steady progress, and building solutions that can grow smoothly as your business evolves. We use modern technologies to create fast, responsive, and secure applications with clean architecture and scalable performance.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Understand Your Needs",
                'description': "We start by understanding your business, challenges, and expectations. This helps us stay aligned and avoid unnecessary work."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Plan with You",
                'description': "Together, we decide what features are needed and how the application should function. This keeps the project clear and avoids confusion."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "Design for Ease of Use",
                'description': "We design the application so it feels simple and natural for users. Clear layouts and smooth flow help people get things done without frustration."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/testing-assurance-image.png",
                'title': "Build An Application",
                'description': "Using the MERN stack, we develop the application step by step. We keep everything organized so updates and changes are easier to manage."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/launch-icon.png",
                'title': "Review Before Launch",
                'description': "We check the application to make sure it works properly and feels stable for everyday use. Any issues are addressed before going live."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/maintenance-and-optimization.png",
                'title': "Launch and Ongoing Support",
                'description': "We support you during launch and remain available afterward for updates, fixes, or improvements as your needs change."
            }
        ]
    },
    'content-strategy': {
        'title': "Best Content Strategy Company",
        'cover_image': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
        'intro_text': "At Sortiq Solutions Pvt. Ltd., we craft impactful content strategies designed to communicate your brand's story effectively and build deep engagement with your target audience. We map out content calendars, write optimized blogs, structure corporate communication scripts, and design user-focused copies.",
        'cards': [
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/discover-and-strategy.png",
                'title': "Audience Research",
                'description': "We identify user personas, search intents, and communication channels to align content themes directly with what your audience values."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/wireframing-design.png",
                'title': "Copywriting & Editing",
                'description': "Our professional writers produce highly engaging copy for websites, newsletters, corporate pitches, and landing pages."
            },
            {
                'icon': "https://sortiqsolutions.com/wp-content/uploads/2025/02/development-coding.png",
                'title': "SEO Content Planning",
                'description': "We plan and write blogs matching technical ranking guidelines to capture search traffic and scale domain authority."
            }
        ]
    }
}

@app.route('/terms/')
@app.route('/faq/')
@app.route('/support/')
@app.route('/privacy-policy/')
@app.route('/website-designing-company/')
@app.route('/website-development-company/')
@app.route('/seo-company/')
@app.route('/smo-company/')
@app.route('/digital-marketing-company/')
@app.route('/ecommerce-development-company/')
@app.route('/bigcommerce-development-company/')
@app.route('/mern-stack-development-company/')
@app.route('/app-development-company/')
@app.route('/software-testing-company/')
@app.route('/website-maintenance-company/')
@app.route('/website-maintenance/')
@app.route('/cyber-security-development/')
@app.route('/hubspot-crm-services/')
@app.route('/zoho-crm-services/')
@app.route('/php-development-company/')
@app.route('/laravel-development-company/')
@app.route('/codeigniter-development-company/')
@app.route('/shopify-development-company/')
@app.route('/wordpress-development-company/')
@app.route('/react-js-development-company/')
@app.route('/node-js-development-company/')
@app.route('/vue-js-development-company/')
@app.route('/graphic-designing-company/')
@app.route('/logo-designing-company/')
@app.route('/banner-designing-company/')
@app.route('/data-science-development/')
@app.route('/website-development/')
@app.route('/graphic-design/')
@app.route('/digital-marketing/')
@app.route('/content-strategy/')
@app.route('/laravel-development/')
@app.route('/wordpress-development/')
@app.route('/mern-stack/')
def dynamic_pages():
    path = request.path.strip('/')
    if path == 'website-maintenance':
        path = 'website-maintenance-company'
    page_info = DYNAMIC_PAGES.get(path)
    if not page_info:
        return redirect(url_for('index'))
    return render_template('generic_page.html', **page_info)


@app.route('/portfolios/')
def portfolios():
    return render_template('portfolio.html')

@app.route('/case-studies/')
def case_studies():
    return render_template('case_studies.html')

@app.route('/blog/')
@app.route('/blog/page/<int:page>/')
def blog(page=1):
    posts = load_blogs()
    posts_per_page = 4
    total_posts = len(posts)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page
    
    if page < 1 or (page > total_pages and total_pages > 0):
        return redirect('/blog/')
        
    start_idx = (page - 1) * posts_per_page
    end_idx = start_idx + posts_per_page
    page_posts = posts[start_idx:end_idx]
    
    return render_template('blog.html', posts=page_posts, current_page=page, total_pages=total_pages)

@app.route('/blog/<slug>/')
def blog_detail(slug):
    posts = load_blogs()
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        return redirect(url_for('blog'))
    return render_template('blog_detail.html', post=post)

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/internship/')
def internship():
    return render_template('internship.html')

# Videos data matching the official gallery pages
VIDEOS_DATA = {
    1: [
        {"title": "Sortiq Solutions: Smart Sorting", "src": "https://www.youtube.com/embed/NrRXiSe13EI?si=ccJ_7hhoQG7jCgeW"},
        {"title": "Welcome to Sortiq Solutions - Sortiq Solutions Pvt. Ltd.", "src": "https://www.youtube.com/embed/s38x-5_kwlI?si=qmKmVIC8NXJDAo60"},
        {"title": "Web Design Services That Elevate Your Brand", "src": "https://www.youtube.com/embed/wAXiBG9UVSY"}
    ],
    2: [
        {"title": "Grow Your Business with Expert Digital Marketing!", "src": "https://www.youtube.com/embed/--2kShqa1Cs"},
        {"title": "Unleash Creativity with Stunning Graphic Design Services!", "src": "https://www.youtube.com/embed/q1Vgfz_KXjA"},
        {"title": "Revolutionize Your Business with Custom Mobile App Development!", "src": "https://www.youtube.com/embed/utYPlOVZWLs"}
    ]
}

@app.route('/video/')
@app.route('/videos/')
@app.route('/videos/page/<int:page>/')
def videos(page=1):
    if page not in VIDEOS_DATA:
        return redirect('/videos/')
    return render_template('video.html', videos=VIDEOS_DATA[page], current_page=page)


# Form submissions
@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    try:
        data = request.form
        name = data.get('name') or data.get('your-name')
        email = data.get('email')
        phone = data.get('phone')
        subject = data.get('subject')
        message = data.get('message')
        
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Name and Email are required.'}), 400
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO enquiries (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)',
            (name, email, phone, subject, message)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Thank you! Your enquiry has been received.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server Error: {str(e)}'}), 500

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.form
        name = data.get('name') or data.get('your-name')
        email = data.get('email')
        phone = data.get('phone')
        subject = data.get('subject')
        message = data.get('message')
        
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Name and Email are required.'}), 400
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO enquiries (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)',
            (name, email, phone, subject, message)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Message sent successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server Error: {str(e)}'}), 500

@app.route('/submit-fresher', methods=['POST'])
def submit_fresher():
    try:
        data = request.form
        name = data.get('name') or data.get('your-name')
        email = data.get('email')
        phone = data.get('phone')
        subject = data.get('subject')
        institute = data.get('institute', '')
        technology = data.get('technology', '')
        message = data.get('message')
        
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Name and Email are required.'}), 400
            
        cv_file = request.files.get('cv')
        cv_filename = None
        if cv_file and cv_file.filename != '':
            original_filename = secure_filename(cv_file.filename)
            import time
            cv_filename = f"{int(time.time())}_{original_filename}"
            cv_file.save(os.path.join(UPLOAD_FOLDER, cv_filename))
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO fresher_applications (name, email, phone, subject, institute, technology, message, cv_filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, email, phone, subject, institute, technology, message, cv_filename)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Application submitted successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server Error: {str(e)}'}), 500


# Admin Panel Authentication & Management
from functools import wraps
from flask import session

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username') or request.form.get('email')
        password = request.form.get('password')
        
        if (username == 'admin' or username == 'sortiqsolutions@gmail.com' ) and (password == 'sortiq'):
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('admin_login.html')

@app.route('/admin/logout')
@app.route('/admin/logout/')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Successfully logged out.', 'success')
    return redirect(url_for('admin_login'))

@app.context_processor
def inject_globals():
    try:
        conn = get_db_connection()
        settings_rows = conn.execute('SELECT * FROM site_settings').fetchall()
        conn.close()
        settings = {row['key']: row['value'] for row in settings_rows}
        
        import copy
        site_layout = copy.deepcopy(DEFAULT_SITE_LAYOUT)
        if 'site_layout' in settings:
            try:
                loaded = json.loads(settings['site_layout'])
                if loaded:
                    site_layout.update(loaded)
            except Exception:
                pass
                
        # Pad nav_links to always have at least 8 elements to prevent Jinja index errors
        nav_links = site_layout.get('nav_links', [])
        while len(nav_links) < 8:
            nav_links.append({"label": "", "url": "", "has_dropdown": "0"})
        site_layout['nav_links'] = nav_links
        
        # Pad footer_badges to always have at least 8 elements
        badges = site_layout.get('footer_badges', [])
        while len(badges) < 8:
            badges.append({"label": "", "image": ""})
        site_layout['footer_badges'] = badges
        
        return {
            'phone': site_layout['header'].get('phone', '+91 9646522110'),
            'email': site_layout['header'].get('email', 'info@sortiqsolutions.com'),
            'address': site_layout['footer'].get('address', 'IT Park, Block B, Chandigarh, India'),
            'site_layout': site_layout
        }
    except Exception:
        return {
            'phone': '+91 9646522110',
            'email': 'info@sortiqsolutions.com',
            'address': 'IT Park, Block B, Chandigarh, India',
            'site_layout': DEFAULT_SITE_LAYOUT
        }

@app.route('/admin/dashboard')
@app.route('/admin/dashboard/')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    enquiries_rows = conn.execute('SELECT * FROM enquiries ORDER BY timestamp DESC').fetchall()
    applications_rows = conn.execute('SELECT * FROM fresher_applications ORDER BY timestamp DESC').fetchall()
    
    enquiries = [dict(row) for row in enquiries_rows]
    applications = [dict(row) for row in applications_rows]
    
    enquiries_count = len(enquiries)
    applications_count = len(applications)
    resumes_count = conn.execute('SELECT COUNT(*) FROM fresher_applications WHERE cv_filename IS NOT NULL AND cv_filename != ""').fetchone()[0]
    
    # Load from DB tables
    blogs = [dict(r) for r in conn.execute('SELECT * FROM blogs ORDER BY id DESC').fetchall()]
    for b in blogs:
        b['categories'] = [c.strip() for c in b['categories'].split(',')] if b['categories'] else []
        
    reviews = [dict(r) for r in conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()]
    portfolios = [dict(r) for r in conn.execute('SELECT * FROM portfolios ORDER BY id DESC').fetchall()]
    videos = [dict(r) for r in conn.execute('SELECT * FROM videos ORDER BY id DESC').fetchall()]
    client_logos = [dict(r) for r in conn.execute('SELECT * FROM client_logos ORDER BY id DESC').fetchall()]
    pages_meta = [dict(r) for r in conn.execute('SELECT * FROM pages_metadata').fetchall()]
    settings_rows = conn.execute('SELECT * FROM site_settings').fetchall()
    settings = {row['key']: row['value'] for row in settings_rows}
    
    conn.close()
    
    blogs_count = len(blogs)
    reviews_count = len(reviews)
    logos_count = len(client_logos)
    videos_count = len(videos)
    portfolios_count = len(portfolios)
    
    return render_template(
        'admin_dashboard.html',
        enquiries=enquiries,
        applications=applications,
        enquiries_count=enquiries_count,
        applications_count=applications_count,
        resumes_count=resumes_count,
        blogs=blogs,
        reviews=reviews,
        portfolios=portfolios,
        videos=videos,
        client_logos=client_logos,
        pages_metadata=pages_meta,
        site_settings=settings,
        blogs_count=blogs_count,
        reviews_count=reviews_count,
        logos_count=logos_count,
        videos_count=videos_count,
        portfolios_count=portfolios_count
    )

@app.route('/admin/delete-enquiry/<int:id>', methods=['POST'])
@admin_required
def delete_enquiry(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM enquiries WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Enquiry successfully deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting enquiry: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-fresher/<int:id>', methods=['POST'])
@admin_required
def delete_fresher(id):
    try:
        conn = get_db_connection()
        app_row = conn.execute('SELECT cv_filename FROM fresher_applications WHERE id = ?', (id,)).fetchone()
        if app_row and app_row['cv_filename']:
            file_path = os.path.join(UPLOAD_FOLDER, app_row['cv_filename'])
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as file_err:
                    print(f"Error removing file: {file_err}")
                
        conn.execute('DELETE FROM fresher_applications WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Application successfully deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting application: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Blogs CRUD
@app.route('/admin/blogs/add', methods=['POST'])
@admin_required
def add_blog():
    try:
        title = request.form.get('title')
        slug = request.form.get('slug') or title.lower().replace(' ', '-')
        category = request.form.get('category', 'Technology')
        summary = request.form.get('summary', '')
        image = request.form.get('image', '')
        content = request.form.get('content', '')
        
        import datetime
        date_str = datetime.datetime.now().strftime("%B %Y")
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO blogs (title, slug, date, categories, summary, image, content) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, slug, date_str, category, summary, image, content)
        )
        conn.commit()
        conn.close()
        flash('Blog post published successfully!', 'success')
    except Exception as e:
        flash(f'Error publishing blog: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/blogs/edit/<int:id>', methods=['POST'])
@admin_required
def edit_blog(id):
    try:
        title = request.form.get('title')
        slug = request.form.get('slug')
        category = request.form.get('category')
        summary = request.form.get('summary')
        image = request.form.get('image')
        content = request.form.get('content')
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE blogs SET title = ?, slug = ?, categories = ?, summary = ?, image = ?, content = ? WHERE id = ?',
            (title, slug, category, summary, image, content, id)
        )
        conn.commit()
        conn.close()
        flash('Blog post updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating blog: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/blogs/delete/<int:id>', methods=['POST'])
@admin_required
def delete_blog(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM blogs WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Blog post deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting blog: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Reviews CRUD
@app.route('/admin/reviews/add', methods=['POST'])
@admin_required
def add_review():
    try:
        author = request.form.get('author')
        platform = request.form.get('platform', 'Google')
        text = request.form.get('text')
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO reviews (author, platform, text) VALUES (?, ?, ?)',
            (author, platform, text)
        )
        conn.commit()
        conn.close()
        flash('Review added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding review: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reviews/edit/<int:id>', methods=['POST'])
@admin_required
def edit_review(id):
    try:
        author = request.form.get('author')
        platform = request.form.get('platform')
        text = request.form.get('text')
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE reviews SET author = ?, platform = ?, text = ? WHERE id = ?',
            (author, platform, text, id)
        )
        conn.commit()
        conn.close()
        flash('Review updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating review: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reviews/delete/<int:id>', methods=['POST'])
@admin_required
def delete_review(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM reviews WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Review deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting review: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Portfolios CRUD
@app.route('/admin/portfolio/add', methods=['POST'])
@admin_required
def add_portfolio():
    try:
        title = request.form.get('title')
        tech = request.form.get('technology')
        loc = request.form.get('location')
        stat = request.form.get('status', 'Completed')
        
        conn = get_db_connection()
        max_id_row = conn.execute('SELECT MAX(id) FROM portfolios').fetchone()
        next_id = (max_id_row[0] or 0) + 1
        pcode = f"#PRJ-{next_id:03d}"
        
        conn.execute(
            'INSERT INTO portfolios (project_code, title, technology, location, status) VALUES (?, ?, ?, ?, ?)',
            (pcode, title, tech, loc, stat)
        )
        conn.commit()
        conn.close()
        flash('Portfolio project added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding project: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/portfolio/edit/<int:id>', methods=['POST'])
@admin_required
def edit_portfolio(id):
    try:
        title = request.form.get('title')
        tech = request.form.get('technology')
        loc = request.form.get('location')
        stat = request.form.get('status')
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE portfolios SET title = ?, technology = ?, location = ?, status = ? WHERE id = ?',
            (title, tech, loc, stat, id)
        )
        conn.commit()
        conn.close()
        flash('Portfolio project updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating project: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/portfolio/delete/<int:id>', methods=['POST'])
@admin_required
def delete_portfolio(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM portfolios WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Portfolio project deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting project: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Videos CRUD
@app.route('/admin/videos/add', methods=['POST'])
@admin_required
def add_video():
    try:
        title = request.form.get('title')
        src = request.form.get('src')
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO videos (title, src) VALUES (?, ?)',
            (title, src)
        )
        conn.commit()
        conn.close()
        flash('Video entry added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding video: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/videos/delete/<int:id>', methods=['POST'])
@admin_required
def delete_video(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM videos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Video entry deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting video: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Logos CRUD
@app.route('/admin/logos/add', methods=['POST'])
@admin_required
def add_logo():
    try:
        url = request.form.get('url', '')
        logo_file = request.files.get('logo_file')
        if logo_file and logo_file.filename:
            filename = secure_filename(logo_file.filename)
            upload_path = os.path.join(app.root_path, 'static', 'images')
            os.makedirs(upload_path, exist_ok=True)
            logo_file.save(os.path.join(upload_path, filename))
            url = '/static/images/' + filename
        
        if not url:
            raise Exception("Please select a file or enter a logo URL")
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO client_logos (url) VALUES (?)',
            (url,)
        )
        conn.commit()
        conn.close()
        flash('Partner logo added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding partner logo: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/logos/delete/<int:id>', methods=['POST'])
@admin_required
def delete_logo(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM client_logos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Partner logo deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting partner logo: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Pages Metadata Update
@app.route('/admin/pages/update', methods=['POST'])
@admin_required
def update_pages_meta():
    try:
        page_path = request.form.get('page_path')
        title = request.form.get('title')
        description = request.form.get('description')
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO pages_metadata (page_path, title, description) VALUES (?, ?, ?) '
            'ON CONFLICT(page_path) DO UPDATE SET title=excluded.title, description=excluded.description',
            (page_path, title, description)
        )
        conn.commit()
        conn.close()
        flash('Page metadata settings updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating metadata: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Site Settings Update
@app.route('/admin/settings/update', methods=['POST'])
@admin_required
def update_site_settings():
    try:
        conn = get_db_connection()
        row = conn.execute("SELECT value FROM site_settings WHERE key = 'site_layout'").fetchone()
        
        layout = DEFAULT_SITE_LAYOUT.copy()
        if row:
            try:
                layout = json.loads(row['value'])
            except:
                pass
                
        # 1. Update header
        layout['header']['logo_text'] = request.form.get('header[logo_text]', layout['header'].get('logo_text', ''))
        layout['header']['phone'] = request.form.get('header[phone]', layout['header'].get('phone', ''))
        layout['header']['email'] = request.form.get('header[email]', layout['header'].get('email', ''))
        layout['header']['apply_label'] = request.form.get('header[apply_label]', layout['header'].get('apply_label', ''))
        layout['header']['apply_url'] = request.form.get('header[apply_url]', layout['header'].get('apply_url', ''))

        # Handle header logo file upload
        logo_file = request.files.get('header_logo_file')
        if logo_file and logo_file.filename:
            filename = secure_filename(logo_file.filename)
            upload_path = os.path.join(app.root_path, 'static', 'images')
            os.makedirs(upload_path, exist_ok=True)
            logo_file.save(os.path.join(upload_path, filename))
            layout['header']['logo'] = '/static/images/' + filename

        # 2. Update nav links
        new_nav_links = []
        for i in range(8):
            label = request.form.get(f'nav_links[{i}][label]')
            url = request.form.get(f'nav_links[{i}][url]')
            has_dropdown = request.form.get(f'nav_links[{i}][has_dropdown]', '0')
            if label is not None:
                new_nav_links.append({
                    'label': label,
                    'url': url or '',
                    'has_dropdown': has_dropdown
                })
        if new_nav_links:
            layout['nav_links'] = new_nav_links

        # 3. Update footer badges
        new_badges = []
        for i in range(8):
            label = request.form.get(f'footer_badges[{i}][label]', '')
            badge_file = request.files.get(f'footer_badge_files[{i}]')
            existing_image = layout['footer_badges'][i]['image'] if i < len(layout['footer_badges']) else ''
            
            if badge_file and badge_file.filename:
                filename = secure_filename(badge_file.filename)
                upload_path = os.path.join(app.root_path, 'static', 'images')
                os.makedirs(upload_path, exist_ok=True)
                badge_file.save(os.path.join(upload_path, filename))
                image_url = '/static/images/' + filename
            else:
                image_url = existing_image

            new_badges.append({
                'label': label,
                'image': image_url
            })
        layout['footer_badges'] = new_badges

        # 4. Update footer contacts
        layout['footer']['address'] = request.form.get('footer[address]', layout['footer'].get('address', ''))
        layout['footer']['phone'] = request.form.get('footer[phone]', layout['footer'].get('phone', ''))
        layout['footer']['email'] = request.form.get('footer[email]', layout['footer'].get('email', ''))
        layout['footer']['certificate_text'] = request.form.get('footer[certificate_text]', layout['footer'].get('certificate_text', ''))
        layout['footer']['certificate_button_label'] = request.form.get('footer[certificate_button_label]', layout['footer'].get('certificate_button_label', ''))
        layout['footer']['certificate_url'] = request.form.get('footer[certificate_url]', layout['footer'].get('certificate_url', ''))
        layout['footer']['chat_label'] = request.form.get('footer[chat_label]', layout['footer'].get('chat_label', ''))
        layout['footer']['chat_url'] = request.form.get('footer[chat_url]', layout['footer'].get('chat_url', ''))

        # 5. Update footer columns (company, services, solutions)
        for col in ['company', 'services', 'solutions']:
            title = request.form.get(f'footer_columns[{col}][title]')
            if title is not None:
                if col not in layout['footer_columns']:
                    layout['footer_columns'][col] = {'title': title, 'links': []}
                else:
                    layout['footer_columns'][col]['title'] = title
            
            new_links = []
            for j in range(12):
                lbl = request.form.get(f'footer_columns[{col}][links][{j}][label]')
                url = request.form.get(f'footer_columns[{col}][links][{j}][url]')
                if lbl is not None:
                    new_links.append({
                        'label': lbl,
                        'url': url or ''
                    })
            if new_links:
                layout['footer_columns'][col]['links'] = new_links

        # Save back to DB
        conn.execute(
            "INSERT INTO site_settings (key, value) VALUES ('site_layout', ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (json.dumps(layout),)
        )
        conn.commit()
        conn.close()
        flash('Site layout settings updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating site settings: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/reviews/')
@app.route('/reviews/page/<int:page>/')
def reviews(page=1):
    all_reviews = load_reviews()
    reviews_per_page = 12
    total_reviews = len(all_reviews)
    total_pages = (total_reviews + reviews_per_page - 1) // reviews_per_page
    
    if page < 1 or (page > total_pages and total_pages > 0):
        return redirect('/reviews/')
        
    start_idx = (page - 1) * reviews_per_page
    end_idx = start_idx + reviews_per_page
    page_reviews = all_reviews[start_idx:end_idx]
    
    return render_template('reviews.html', reviews=page_reviews, current_page=page, total_pages=total_pages)

@app.route('/reviews/ajax/<int:page>')
def reviews_ajax(page):
    all_reviews = load_reviews()
    reviews_per_page = 12
    total_reviews = len(all_reviews)
    total_pages = (total_reviews + reviews_per_page - 1) // reviews_per_page
    
    if page < 1 or page > total_pages:
        return ""
        
    start_idx = (page - 1) * reviews_per_page
    end_idx = start_idx + reviews_per_page
    page_reviews = all_reviews[start_idx:end_idx]
    
    return render_template('reviews_partial.html', reviews=page_reviews, current_page=page, total_pages=total_pages)

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
