from html.parser import HTMLParser
import hashlib
from pathlib import Path
import unittest


PORTFOLIO_ROOT = Path(__file__).resolve().parents[1]
V2_HTML = PORTFOLIO_ROOT / "index.html"
V2_CSS = PORTFOLIO_ROOT / "styles.css"
ARCHIVED_HTML = PORTFOLIO_ROOT / "archive" / "index-original.html"
ARCHIVED_CSS = PORTFOLIO_ROOT / "archive" / "styles-original.css"


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
        self.assertTrue(V2_HTML.exists(), "index.html must exist")
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
            {widget["attrs"].get("agent-id") for widget in widgets},
            {"agent_9501m3kf78y2f6cbaz4tym7zs8r9"},
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
        assistant_widget = parser.find_all(
            "elevenlabs-convai", class_name="floating-ai-assistant"
        )[0]
        self.assertEqual(
            assistant_widget["attrs"].get("action-text"),
            "Ask My AI Assistant",
        )

    def test_v2_uses_one_unconstrained_floating_assistant(self):
        parser = self.parse_v2()
        embedded = parser.find_all(
            "elevenlabs-convai", class_name="embedded-ai-assistant"
        )
        floating = parser.find_all(
            "elevenlabs-convai", class_name="floating-ai-assistant"
        )
        launchers = parser.find_all("button", class_name="ai-widget-open")
        docks = parser.find_all("div", element_id="ai-assistant-dock")

        self.assertEqual(len(embedded), 0)
        self.assertEqual(len(floating), 1)
        self.assertEqual(floating[0]["attrs"].get("variant"), "compact")
        self.assertEqual(floating[0]["attrs"].get("id"), "ai-assistant-widget")
        self.assertEqual(
            floating[0]["attrs"].get("action-text"),
            "Ask My AI Assistant",
        )
        self.assertEqual(len(launchers), 0)
        self.assertEqual(len(docks), 0)

        ai_section = parser.find_all("section", element_id="ai-secretary")[0]
        ai_text = parser.text(ai_section)
        usage_guides = parser.find_all("div", class_name="ai-widget")
        self.assertEqual(len(usage_guides), 1)
        self.assertEqual(
            usage_guides[0]["attrs"].get("aria-label"),
            "How to use the floating AI Assistant",
        )
        self.assertIn("Ask My AI Assistant", ai_text)
        self.assertIn("How to use it", ai_text)
        self.assertIn("Find the floating assistant in the lower-right corner.", ai_text)
        self.assertIn("Choose Start a call for voice or the message bubble for text.", ai_text)
        self.assertIn("Allow microphone access when your browser asks.", ai_text)

        self.assertEqual(len(parser.find_all("div", class_name="ai-chat-modes")), 0)
        self.assertEqual(len(parser.find_all("figure", class_name="ai-widget-guide")), 1)
        guide_images = parser.find_all("img", class_name="ai-widget-guide-image")
        self.assertEqual(len(guide_images), 1)
        self.assertEqual(
            guide_images[0]["attrs"].get("src"),
            "images/ai-assistant-widget-guide.png",
        )
        self.assertEqual(
            guide_images[0]["attrs"].get("alt"),
            "The floating AI assistant with Start a call and text chat controls",
        )
        guide_asset = PORTFOLIO_ROOT / guide_images[0]["attrs"]["src"]
        self.assertTrue(guide_asset.exists())

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

    def test_v2_leaves_the_elevenlabs_overlay_unconstrained(self):
        css = V2_CSS.read_text(encoding="utf-8")
        self.assertNotIn(".ai-widget elevenlabs-convai", css)
        self.assertNotIn(".floating-ai-assistant", css)
        self.assertNotIn(".ai-widget-dock", css)
        self.assertNotIn("--elevenlabs-convai-widget-width", css)
        self.assertNotIn("--elevenlabs-convai-widget-height", css)

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
                "styles.css",
            ],
        )

    def test_original_portfolio_files_are_preserved_in_the_archive(self):
        self.assertTrue(ARCHIVED_HTML.exists())
        self.assertTrue(ARCHIVED_CSS.exists())
        self.assertEqual(
            hashlib.sha256(ARCHIVED_HTML.read_bytes()).hexdigest(),
            "d8f57a27478b52f7f03683f29ccb9fc9b3d27d36a2fb60492b11fc63253b232a",
        )
        self.assertEqual(
            hashlib.sha256(ARCHIVED_CSS.read_bytes()).hexdigest(),
            "bf03e7b285b95ab044754a2bde14ababe8d918231198e5c17d4b576e1e79ccaf",
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
