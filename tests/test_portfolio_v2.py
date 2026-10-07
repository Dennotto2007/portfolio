from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


PORTFOLIO_ROOT = Path(__file__).resolve().parents[1]
V2_HTML = PORTFOLIO_ROOT / "index-v2.html"
V2_CSS = PORTFOLIO_ROOT / "styles-v2.css"


class PortfolioParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        element = {
            "tag": tag,
            "attrs": dict(attrs),
            "text_parts": [],
            "ancestor_ids": [ancestor["attrs"].get("id") for ancestor in self.stack],
        }
        self.elements.append(element)
        for ancestor in self.stack:
            ancestor["text_parts"].append("")
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1]["tag"] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        for element in self.stack:
            element["text_parts"].append(data)

    def find_all(self, tag=None, *, element_id=None, class_name=None):
        matches = []
        for element in self.elements:
            attrs = element["attrs"]
            classes = attrs.get("class", "").split()
            if tag is not None and element["tag"] != tag:
                continue
            if element_id is not None and attrs.get("id") != element_id:
                continue
            if class_name is not None and class_name not in classes:
                continue
            matches.append(element)
        return matches

    @staticmethod
    def text(element):
        return " ".join("".join(element["text_parts"]).split())


class PortfolioV2Tests(unittest.TestCase):
    def parse_v2(self):
        self.assertTrue(V2_HTML.exists(), "index-v2.html must exist")
        parser = PortfolioParser()
        parser.feed(V2_HTML.read_text(encoding="utf-8"))
        return parser

    def test_v2_uses_outcome_led_section_order(self):
        parser = self.parse_v2()
        section_ids = [element["attrs"].get("id") for element in parser.find_all("section")]
        self.assertEqual(
            section_ids,
            [
                "hero",
                "proof",
                "companies",
                "ai-secretary",
                "product-work",
                "about",
                "experience",
                "prototypes",
                "skills",
                "education",
                "contact",
            ],
        )

    def test_v2_hero_and_proof_points_match_positioning(self):
        parser = self.parse_v2()
        hero = parser.find_all("section", element_id="hero")[0]
        proof = parser.find_all("section", element_id="proof")[0]
        hero_text = parser.text(hero)
        proof_text = parser.text(proof)
        self.assertIn("Senior Product Manager | Product Builder", hero_text)
        self.assertIn(
            "I build and scale digital products at the intersection of customer experience, business impact, data, and technology.",
            hero_text,
        )
        for metric in ("$10.8M", "€2.5M", "+46%", "70%"):
            with self.subTest(metric=metric):
                self.assertIn(metric, proof_text)

    def test_v2_keeps_ai_assistant_prominent_and_bookable(self):
        parser = self.parse_v2()
        widgets = parser.find_all("elevenlabs-convai")
        self.assertEqual(len(widgets), 1)
        self.assertEqual(
            widgets[0]["attrs"].get("agent-id"),
            "agent_9501m3kf78y2f6cbaz4tym7zs8r9",
        )
        ai_section = parser.find_all("section", element_id="ai-secretary")[0]
        ai_text = parser.text(ai_section)
        self.assertIn("AI Assistant", ai_text)
        self.assertIn("Book a Call", ai_text)
        calendar_links = [
            link
            for link in parser.find_all("a")
            if "calendar.google.com/calendar/appointments/schedules/" in link["attrs"].get("href", "")
        ]
        self.assertGreaterEqual(len(calendar_links), 2)

    def test_v2_uses_natural_ai_assistant_copy(self):
        parser = self.parse_v2()
        ai_section = parser.find_all("section", element_id="ai-secretary")[0]
        ai_text = parser.text(ai_section)
        self.assertIn("Talk to My AI Assistant", ai_text)
        self.assertIn(
            "Ask about my experience, projects, product work, or availability. "
            "My AI assistant can answer questions and help you schedule a call.",
            ai_text,
        )
        widget = parser.find_all("elevenlabs-convai")[0]
        self.assertEqual(widget["attrs"].get("action-text"), "Talk to My AI Assistant")

    def test_v2_loads_the_compatible_elevenlabs_widget_embed(self):
        parser = self.parse_v2()
        widget_scripts = [
            script
            for script in parser.find_all("script")
            if script["attrs"].get("src")
            == "https://unpkg.com/@elevenlabs/convai-widget-embed"
            and "async" in script["attrs"]
        ]
        self.assertEqual(len(widget_scripts), 1)

    def test_v2_contains_the_elevenlabs_widget_inside_its_panel(self):
        css = V2_CSS.read_text(encoding="utf-8")

        def declarations_for(selector):
            match = re.search(
                rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]+)\}}",
                css,
                flags=re.MULTILINE,
            )
            self.assertIsNotNone(match, f"Missing CSS rule for {selector}")
            declarations = {}
            for declaration in match.group("body").split(";"):
                if ":" not in declaration:
                    continue
                property_name, value = declaration.split(":", 1)
                declarations[property_name.strip()] = value.strip()
            return declarations

        panel = declarations_for(".ai-widget")
        widget = declarations_for(".ai-widget elevenlabs-convai")
        self.assertEqual(panel.get("position"), "relative")
        self.assertEqual(panel.get("overflow"), "hidden")
        self.assertEqual(widget.get("position"), "relative")
        self.assertEqual(widget.get("inset"), "auto")
        self.assertEqual(widget.get("display"), "block")
        self.assertEqual(widget.get("width"), "100%")
        self.assertEqual(widget.get("--elevenlabs-convai-widget-width"), "100%")
        self.assertEqual(widget.get("--elevenlabs-convai-widget-height"), "22rem")

    def test_v2_contains_three_selected_product_case_studies(self):
        parser = self.parse_v2()
        case_studies = parser.find_all("article", class_name="case-study")
        self.assertEqual(
            [case["attrs"].get("id") for case in case_studies],
            ["groupon-gifting", "groupon-monetization", "toptal-experimentation"],
        )
        for case in case_studies:
            case_text = parser.text(case)
            with self.subTest(case=case["attrs"].get("id")):
                self.assertIn("Context", case_text)
                self.assertIn("Contribution", case_text)
                self.assertIn("Outcome", case_text)

    def test_v2_contains_prototypes_skills_and_compact_education(self):
        parser = self.parse_v2()
        prototypes = parser.text(parser.find_all("section", element_id="prototypes")[0])
        for label in (
            "Website Summary Tool",
            "Matrix Notes Flow",
            "AI SEO Automation",
            "AI Product Development & Automation",
        ):
            with self.subTest(prototype=label):
                self.assertIn(label, prototypes)

        skills = parser.text(parser.find_all("section", element_id="skills")[0])
        for label in (
            "Product Strategy & Discovery",
            "AI & Automation",
            "Experimentation",
            "Growth & Monetization",
            "Platform Products",
            "Customer Experience",
            "Data & Analytics",
            "Marketplace & SaaS",
        ):
            with self.subTest(skill=label):
                self.assertIn(label, skills)

        education_items = parser.find_all("article", class_name="education-item")
        self.assertEqual(len(education_items), 2)

    def test_v2_external_links_are_safe(self):
        parser = self.parse_v2()
        external_links = [
            element
            for element in parser.find_all("a")
            if element["attrs"].get("target") == "_blank"
        ]
        self.assertGreater(len(external_links), 0)
        for link in external_links:
            rel_values = set(link["attrs"].get("rel", "").split())
            with self.subTest(href=link["attrs"].get("href")):
                self.assertTrue({"noopener", "noreferrer"}.issubset(rel_values))

    def test_v2_navigation_exposes_accessible_mobile_state(self):
        parser = self.parse_v2()
        toggles = parser.find_all("button", class_name="nav-toggle")
        self.assertEqual(len(toggles), 1)
        self.assertEqual(toggles[0]["attrs"].get("aria-controls"), "primary-navigation")
        self.assertEqual(toggles[0]["attrs"].get("aria-expanded"), "false")

        nav_lists = parser.find_all("ul", element_id="primary-navigation")
        self.assertEqual(len(nav_lists), 1)
        expected_links = [
            ("#product-work", "Product Work"),
            ("#about", "About"),
            ("#experience", "Experience"),
            ("#prototypes", "AI & Prototypes"),
            ("#skills", "Skills"),
            ("#contact", "Contact"),
        ]
        section_links = [
            (link["attrs"].get("href"), parser.text(link))
            for link in parser.find_all("a")
            if "primary-navigation" in link["ancestor_ids"]
        ]
        self.assertEqual(section_links, expected_links)

        stylesheet_links = [
            link
            for link in parser.find_all("link")
            if link["attrs"].get("rel") == "stylesheet"
        ]
        self.assertEqual(
            [link["attrs"].get("href") for link in stylesheet_links],
            [
                "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap",
                "styles-v2.css",
            ],
        )

    def test_v2_retains_all_six_approved_experience_roles(self):
        parser = self.parse_v2()
        experience = parser.find_all("section", element_id="experience")[0]
        experience_text = parser.text(experience)
        self.assertEqual(len(parser.find_all("article", class_name="timeline-item")), 6)
        for approved_detail in (
            "Partnered with Engineering, Design, Analytics, Commercial, Marketing, and platform teams across multiple markets",
            "Designed and evaluated A/B experiments across UX, acquisition, and monetization",
            "Applied AI and automation to scale content and growth workflows",
            "Worked across Product, Engineering, Marketing, and Commercial teams",
            "Used customer, commercial, and product data to shape roadmap priorities",
            "Conducted competitive and customer research",
        ):
            with self.subTest(approved_detail=approved_detail):
                self.assertIn(approved_detail, experience_text)

    def test_v2_uses_the_approved_booking_schedule(self):
        parser = self.parse_v2()
        approved_url = (
            "https://calendar.google.com/calendar/appointments/schedules/"
            "AcZssZ0VEUbj0cybjt2SrXryf3jkqBol-_KjExRz75Y3XOEbExl53gnkRuE9zU5nPCBwF9jmbPW3z3Hg"
        )
        calendar_links = [
            link["attrs"].get("href")
            for link in parser.find_all("a")
            if "calendar.google.com/calendar/appointments/schedules/" in link["attrs"].get("href", "")
        ]
        self.assertEqual(calendar_links, [approved_url, approved_url])


if __name__ == "__main__":
    unittest.main()
