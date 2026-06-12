from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_compress import Compress
import os

app = Flask(__name__)
Compress(app)
app.secret_key = 'sortiq_clone_secret_key'

@app.after_request
def add_header(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

import json

def load_blogs():
    json_path = os.path.join(app.root_path, 'static', 'blogs.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_reviews():
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
