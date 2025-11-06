"""
AI Content Generation Engine
Orchestrates calls to multiple LLM APIs with intelligent routing
"""

import os
from typing import Dict, Optional
from .models import Document, Section

# API configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


class AIContentGenerator:
    """Handles AI-powered content generation with multi-model support"""

    def __init__(self, default_model: str = "gpt4", use_mock: bool = None):
        """
        Initialize AI generator

        Args:
            default_model: Default model to use (gpt4, claude, mock)
            use_mock: If True, use mock responses. If None, auto-detect based on API keys
        """
        self.default_model = default_model

        # Auto-detect if we should use mock mode
        if use_mock is None:
            self.use_mock = not (OPENAI_API_KEY or ANTHROPIC_API_KEY)
        else:
            self.use_mock = use_mock

        self.prompt_templates = self._initialize_prompt_templates()
        self.model_config = self._initialize_model_config()

    def _initialize_model_config(self) -> Dict:
        """Initialize available models and their characteristics"""
        return {
            "gpt4": {
                "provider": "openai",
                "model_name": "gpt-4",
                "max_tokens": 8000,
                "strengths": ["detailed generation", "reasoning", "step-by-step procedures"]
            },
            "gpt35": {
                "provider": "openai",
                "model_name": "gpt-3.5-turbo",
                "max_tokens": 4000,
                "strengths": ["general content", "fast responses"]
            },
            "claude": {
                "provider": "anthropic",
                "model_name": "claude-3-sonnet-20240229",
                "max_tokens": 100000,
                "strengths": ["summarization", "detailed analysis", "citations"]
            },
            "mock": {
                "provider": "mock",
                "model_name": "mock",
                "max_tokens": 1000,
                "strengths": ["demo testing"]
            }
        }

    def _initialize_prompt_templates(self) -> Dict[str, str]:
        """Initialize default prompt templates for each section type"""
        return {
            "Purpose": """You are an expert in writing Standard Operating Procedures (SOPs).
Write a clear and concise Purpose section for this SOP.

SOP Title: {topic}
Context: {context}

The Purpose section should:
- Explain WHAT this procedure does
- Explain WHY this procedure is important
- Be 2-4 sentences
- Use formal, professional language

Generate the Purpose section:""",

            "Scope": """Write a Scope section that defines what is included and excluded in this SOP.

SOP Title: {topic}
Context: {context}

The Scope section should:
- Clearly define what is covered
- Specify any limitations or exclusions
- Mention applicable standards or regulations
- Be specific and concise

Generate the Scope section:""",

            "Definitions and Abbreviations": """Provide key definitions and abbreviations for this SOP.

SOP Title: {topic}
Context: {context}

Include:
- Technical terms specific to this procedure
- Abbreviations and acronyms used
- Industry-standard definitions
- Format as a bulleted or numbered list

Generate the Definitions and Abbreviations:""",

            "Responsibilities": """List the roles and their responsibilities in carrying out this SOP.

SOP Title: {topic}
Context: {context}

Include:
- Key personnel roles (Operator, Supervisor, QA, etc.)
- Specific responsibilities for each role
- Use bullet points
- Be clear about who does what

Generate the Responsibilities section:""",

            "Normative References": """List relevant standards, references, and documents applicable to this SOP.

SOP Title: {topic}
Standards: {standards}
Context: {context}

Include:
- International standards (ISO, IEC, ASTM, etc.)
- Internal documents and procedures
- Regulatory requirements
- Use proper citation format

Generate the Normative References section:""",

            "HSE Risk Assessment": """Provide a Health, Safety, and Environment (HSE) risk assessment for this procedure.

SOP Title: {topic}
Context: {context}

Include:
- Potential hazards
- Risk levels (High/Medium/Low)
- Required safety equipment
- Emergency procedures
- Environmental considerations

Generate the HSE Risk Assessment section:""",

            "Equipment and Materials": """List all equipment and materials needed for this procedure.

SOP Title: {topic}
Context: {context}

Include:
- Specific equipment with model/specifications
- Consumable materials
- Calibration requirements
- Quantity requirements

Generate the Equipment and Materials section:""",

            "Test Procedure": """Write a detailed step-by-step test procedure.

SOP Title: {topic}
Context: {context}

Requirements:
- Use numbered steps
- Be clear and unambiguous
- Include critical parameters
- Mention quality checks
- Assume reader has basic technical knowledge

Generate the Test Procedure section:""",

            "Procedure": """Write a detailed step-by-step procedure.

SOP Title: {topic}
Context: {context}

Requirements:
- Use numbered steps
- Be clear and unambiguous
- Include critical parameters
- Mention quality checks

Generate the Procedure section:""",

            "Data Analysis and Requirements": """Describe data analysis methods and requirements.

SOP Title: {topic}
Context: {context}

Include:
- Data collection methods
- Analysis techniques
- Calculations or formulas
- Statistical requirements
- Data recording procedures

Generate the Data Analysis and Requirements section:""",

            "Pass/Fail Criteria": """Define clear pass/fail criteria for this procedure.

SOP Title: {topic}
Context: {context}

Include:
- Specific acceptance criteria
- Quantitative limits or thresholds
- Visual inspection criteria
- References to standards

Generate the Pass/Fail Criteria section:""",

            "Safety Considerations": """Describe safety considerations for this procedure.

SOP Title: {topic}
Context: {context}

Include:
- Hazards and risks
- Required PPE
- Safety protocols
- Emergency procedures

Generate the Safety Considerations section:"""
        }

    def route_model_for_section(self, section_title: str) -> str:
        """
        Decide which model to use for a given section

        Args:
            section_title: Title of the section

        Returns:
            Model key to use
        """
        if self.use_mock:
            return "mock"

        title_lower = section_title.lower()

        # Route based on section characteristics
        if any(word in title_lower for word in ["reference", "normative", "citation"]):
            return "claude" if ANTHROPIC_API_KEY else "gpt4"

        if any(word in title_lower for word in ["procedure", "method", "steps", "test"]):
            return "gpt4" if OPENAI_API_KEY else "claude"

        if any(word in title_lower for word in ["purpose", "scope", "objective"]):
            return "gpt4" if OPENAI_API_KEY else "claude"

        # Default routing
        if OPENAI_API_KEY:
            return "gpt4"
        elif ANTHROPIC_API_KEY:
            return "claude"
        else:
            return "mock"

    def generate_section_content(
        self,
        document: Document,
        section: Section,
        additional_context: str = ""
    ) -> str:
        """
        Generate content for a section using appropriate AI model

        Args:
            document: The document containing this section
            section: The section to generate content for
            additional_context: Additional user instructions

        Returns:
            Generated content string
        """
        # Prepare context
        context = {
            "topic": document.title,
            "standards": document.metadata.get("standards", ""),
            "context": additional_context or document.metadata.get("description", "")
        }

        # Get prompt template
        prompt_template = self.prompt_templates.get(
            section.title,
            "Generate professional content for the '{section_title}' section of this SOP.\n\nSOP Title: {topic}\nContext: {context}"
        )

        prompt = prompt_template.format(
            topic=context["topic"],
            context=context["context"],
            standards=context["standards"],
            section_title=section.title
        )

        # Route to appropriate model
        model_key = self.route_model_for_section(section.title)

        # Generate content
        if model_key == "mock":
            return self._generate_mock_content(section.title, document.title)
        elif model_key in ["gpt4", "gpt35"]:
            return self._generate_openai(prompt, model_key)
        elif model_key == "claude":
            return self._generate_anthropic(prompt)
        else:
            return self._generate_mock_content(section.title, document.title)

    def _generate_openai(self, prompt: str, model_key: str) -> str:
        """Generate content using OpenAI API"""
        try:
            import openai

            openai.api_key = OPENAI_API_KEY
            model_name = self.model_config[model_key]["model_name"]

            response = openai.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an expert technical writer specializing in Standard Operating Procedures."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._generate_mock_content("Error", "OpenAI API call failed")

    def _generate_anthropic(self, prompt: str) -> str:
        """Generate content using Anthropic Claude API"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            print(f"Anthropic API error: {e}")
            return self._generate_mock_content("Error", "Anthropic API call failed")

    def _generate_mock_content(self, section_title: str, doc_title: str) -> str:
        """Generate mock content for testing without API keys"""

        mock_content = {
            "Purpose": f"""This Standard Operating Procedure (SOP) establishes the standardized methodology for {doc_title.lower()}.

The purpose of this procedure is to ensure consistent, reproducible, and compliant execution of the specified operations. This SOP provides clear guidance to personnel performing these activities and ensures adherence to applicable standards and regulatory requirements.""",

            "Scope": f"""This procedure applies to all operations related to {doc_title.lower()} within the organization.

**Included:**
- All testing and qualification activities as specified
- Equipment calibration and maintenance related to this procedure
- Documentation and reporting requirements

**Excluded:**
- Emergency or non-standard procedures (covered by separate SOPs)
- Research and development activities outside standard operations""",

            "Definitions and Abbreviations": """**Definitions:**
- **SOP**: Standard Operating Procedure - A documented procedure describing how to perform specific operations
- **QA**: Quality Assurance - Systematic activities ensuring quality requirements are fulfilled
- **Calibration**: Process of checking and adjusting the accuracy of measuring equipment

**Abbreviations:**
- PPE: Personal Protective Equipment
- HSE: Health, Safety, and Environment
- QC: Quality Control
- STC: Standard Test Conditions""",

            "Responsibilities": """**Test Operator:**
- Execute the test procedure as documented
- Record all observations and measurements
- Report any deviations or anomalies
- Maintain cleanliness of equipment and workspace

**Supervisor/Engineer:**
- Review and verify test data
- Approve deviations from standard procedure
- Ensure proper calibration of equipment
- Technical troubleshooting

**QA Manager:**
- Approve final test reports
- Ensure compliance with standards
- Review and approve SOP revisions
- Audit procedure compliance""",

            "Normative References": """The following standards and documents are referenced in this procedure:

1. ISO/IEC 17025 - General requirements for the competence of testing and calibration laboratories
2. Relevant industry-specific standards (IEC, ASTM, etc.)
3. Internal quality management system procedures
4. Equipment manufacturer's operating manuals
5. Applicable regulatory requirements and guidelines""",

            "HSE Risk Assessment": """**Hazard Identification and Risk Assessment:**

| Hazard | Risk Level | Control Measures |
|--------|-----------|------------------|
| Electrical shock | Medium | Use insulated tools, follow lockout/tagout procedures |
| Chemical exposure | Low | Wear appropriate PPE, ensure adequate ventilation |
| Equipment damage | Low | Follow operating procedures, regular maintenance |
| Data integrity | Medium | Use validated systems, maintain proper documentation |

**Required PPE:**
- Safety glasses
- Lab coat
- Closed-toe shoes
- Gloves (as appropriate for materials)

**Emergency Procedures:**
- Emergency stop buttons located at [specify locations]
- First aid kit available at [specify location]
- Emergency contact numbers posted""",

            "Equipment and Materials": """**Equipment Required:**
1. [Primary test equipment] - Model/Specification
2. [Measurement instruments] - Calibration due date must be current
3. [Data acquisition system] - Software version
4. [Environmental chamber/test fixture] - As applicable

**Materials Required:**
1. Test samples - Prepared according to [reference procedure]
2. Consumables - [List specific items]
3. Calibration standards - Traceable to national/international standards
4. Documentation forms and labels

**Calibration Requirements:**
- All measuring equipment must have current calibration certificates
- Calibration interval: As specified in equipment database
- Calibration records maintained in quality system""",

            "Test Procedure": """**Pre-Test Setup:**
1. Verify all equipment is calibrated and functioning properly
2. Prepare test samples according to specifications
3. Record environmental conditions (temperature, humidity)
4. Complete pre-test checklist

**Test Execution:**
1. Position test sample in fixture according to specifications
2. Configure test parameters:
   - Parameter 1: [value/range]
   - Parameter 2: [value/range]
   - Parameter 3: [value/range]

3. Initiate test sequence and monitor progress
4. Record measurements at specified intervals:
   - Measurement 1: [specification]
   - Measurement 2: [specification]

5. Observe and document any anomalies or deviations

**Post-Test:**
6. Allow equipment to return to safe state
7. Remove and inspect test sample
8. Clean equipment and workspace
9. Complete all documentation
10. File test records according to procedure""",

            "Procedure": """1. Review all relevant documentation and ensure understanding of requirements

2. Gather all necessary equipment and materials

3. Perform equipment setup and verification:
   - Check calibration status
   - Verify proper operation
   - Document equipment IDs

4. Execute the procedure steps in sequence:
   - Follow each step precisely
   - Record all required data
   - Note any deviations

5. Perform quality checks at designated checkpoints

6. Complete procedure and perform cleanup

7. Review and sign off documentation

8. Submit records to appropriate personnel for review""",

            "Data Analysis and Requirements": """**Data Collection:**
- All measurements must be recorded in real-time
- Use calibrated instruments only
- Record to appropriate significant figures
- Note any environmental conditions affecting measurements

**Data Analysis:**
- Calculate required parameters using specified formulas
- Compare results to acceptance criteria
- Perform statistical analysis as required
- Identify any trends or anomalies

**Calculation Example:**
[Parameter] = (Measured Value × Correction Factor) / Reference Value

**Uncertainty Analysis:**
- Estimate measurement uncertainty
- Consider all contributing factors
- Report expanded uncertainty (k=2)

**Data Recording:**
- Use approved data sheets or electronic systems
- Ensure traceability of all measurements
- Maintain data integrity and security""",

            "Pass/Fail Criteria": """**Acceptance Criteria:**

The test sample is considered PASS if all of the following criteria are met:

1. All measured parameters fall within specified limits:
   - Parameter 1: [min value] to [max value]
   - Parameter 2: ≤ [threshold value]
   - Parameter 3: ≥ [minimum value]

2. No visual defects or anomalies observed

3. All quality checks completed successfully

4. No deviations from procedure without approved justification

**The test sample is considered FAIL if:**
- Any parameter falls outside specified limits
- Critical defects are observed
- Required procedure steps were not completed
- Data integrity cannot be verified

**Reporting:**
- PASS results: Issue certificate of conformity
- FAIL results: Issue non-conformance report
- Marginal results: Require engineering review""",

            "Safety Considerations": """**General Safety:**
- All personnel must be trained on this procedure before execution
- Wear required PPE at all times
- Follow lockout/tagout procedures for equipment maintenance
- Report all incidents, near-misses, and safety concerns

**Specific Hazards:**
- [List specific hazards for this procedure]
- [Control measures for each hazard]

**Emergency Procedures:**
- Emergency shutdown: [Specific steps]
- Fire: Activate alarm, evacuate, call emergency services
- Injury: Administer first aid, call for medical assistance
- Spill: Follow spill response procedure, notify supervisor

**Environmental Considerations:**
- Dispose of waste materials according to regulations
- Minimize environmental impact
- Use sustainable practices where possible"""
        }

        # Return specific content or generic
        return mock_content.get(
            section_title,
            f"""[AI-Generated Mock Content for {section_title}]

This section would contain detailed content specific to {section_title} for the SOP titled "{doc_title}".

In production mode with API keys configured, this content would be generated by advanced AI models (GPT-4 or Claude) tailored specifically to your requirements and standards.

**To enable real AI generation:**
1. Add your OpenAI API key: Set OPENAI_API_KEY environment variable
2. Or add Anthropic API key: Set ANTHROPIC_API_KEY environment variable
3. The system will automatically use real AI models when keys are detected

**Current Status:** Running in demo/mock mode for testing purposes."""
        )
