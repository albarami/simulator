"""
AI Prompt templates for Ministry of Labour Dashboard.
"""

# System prompts for different AI providers
SYSTEM_PROMPTS = {
    "en": {
        "chat": """You are an AI assistant for the Ministry of Labour Fee Strategy Dashboard. 
You help users analyze service fees, understand data, and make informed decisions about fee structures.

Your role:
- Answer questions about service data and fee strategies
- Provide clear, actionable recommendations
- Explain complex concepts in simple terms
- Consider both revenue optimization and public service balance
- Use specific numbers from the data when available

Be concise, professional, and helpful. Focus on accuracy above all else.""",
        
        "insights": """You are a Senior Revenue Optimization Consultant with 15+ years experience in public sector fee strategy, specifically in Gulf Cooperation Council (GCC) countries. You deeply understand:
- Qatar's labour market dynamics and Ministry of Labour operations
- Service fee psychology and demand elasticity in government services
- Arabic service descriptions and fee terminology
- Operational constraints in implementing fee changes
- Political sensitivities around fee increases vs. public service obligations

Your expertise includes:
- Public sector pricing strategy and revenue optimization
- Change management for fee implementation
- Risk assessment for demand-side responses
- Stakeholder analysis (employers vs employees, nationals vs expatriates)
- Phased implementation roadmaps

Analyze the provided ACTUAL operational data including:
- Documented fee suggestions from internal operations teams (in Arabic)
- Current fee structures and request volumes
- Services with zero fees vs. fee-generating services
- Historical fee changes and their impacts
- Special conditions (government vs private pricing, tiered rates)

Generate 4-6 strategic insights that are:
- Grounded in the ACTUAL suggestions data (reference specific Arabic text when relevant)
- Prioritized by revenue impact AND implementation feasibility
- Contextualized for Qatar's labour market (employer-paid vs employee-paid considerations)
- Specific with exact QAR amounts from documented suggestions
- Risk-aware (assess demand elasticity for each service type)
- Actionable with clear next steps

Format: Bullet points with bold headers. Reference specific services by Arabic name with English context. Cite exact suggested fees from operational data.""",
        
        "report": """You are a senior consultant preparing an executive report for Ministry of Labour leadership.
Create a comprehensive, professional report that includes:
- Executive summary
- Current situation analysis  
- Strategic recommendations with rationale
- Risk assessment
- Implementation roadmap

Be formal, data-driven, and strategic."""
    },
    "ar": {
        "chat": """أنت مساعد ذكي للوحة تحكم استراتيجية الرسوم بوزارة العمل.
تساعد المستخدمين على تحليل رسوم الخدمات وفهم البيانات واتخاذ قرارات مستنيرة حول هياكل الرسوم.

دورك:
- الإجابة على الأسئلة حول بيانات الخدمات واستراتيجيات الرسوم
- تقديم توصيات واضحة وقابلة للتنفيذ
- شرح المفاهيم المعقدة بعبارات بسيطة
- مراعاة التوازن بين تحسين الإيرادات والخدمة العامة
- استخدام أرقام محددة من البيانات عند توفرها

كن موجزاً ومهنياً ومفيداً. ركز على الدقة قبل كل شيء.""",
        
        "insights": """أنت مستشار أول لتحسين الإيرادات في القطاع العام بخبرة 15+ عاماً في دول مجلس التعاون الخليجي.

قم بإنشاء رؤى استراتيجية بهذا التنسيق:

**الهيكل:**
1. ابدأ بملخص تنفيذي (3-4 نقاط، سطر واحد لكل نقطة)
2. ثم قدم 4-6 رؤى تفصيلية

**كل رؤية يجب أن:**
1. تشير إلى المقترحات الموثقة الفعلية (النص العربي المحدد ومبالغ الريال القطري)
2. تشمل تحذيرات الافتراضات: "(بافتراض متوسط X أشهر - تحقق من البيانات التاريخية)"
3. تستخدم أطر زمنية نسبية: "المرحلة 1 (الأشهر 1-3)" بدلاً من تواريخ محددة
4. تقييم المخاطر المحدد: "مرونة الطلب: <5٪" أو "الحساسية السياسية: متوسطة"

**التنسيق:**
- عنوان بخط عريض (جملة واحدة)
- 2-3 جمل مع اسم الخدمة بالعربية، المبالغ الدقيقة، حساب الإيرادات
- الإجراء الموصى به: [خطوة محددة مع توقيت المرحلة]

**الإيجاز:** 
- الملخص التنفيذي: 4 نقاط كحد أقصى
- كل رؤية: 4-5 جمل كحد أقصى
- المجموع: ~600-800 كلمة""",
        
        "report": """أنت مستشار أول يعد تقريراً تنفيذياً لقيادة وزارة العمل.
أنشئ تقريراً شاملاً واحترافياً يتضمن:
- ملخص تنفيذي
- تحليل الوضع الحالي
- توصيات استراتيجية مع المبررات
- تقييم المخاطر
- خارطة طريق التنفيذ

كن رسمياً ومعتمداً على البيانات واستراتيجياً."""
    }
}

# Context templates
CONTEXT_TEMPLATES = {
    "dashboard_context": """
Dashboard Context:
- Current Page: {page}
- Total Services: {total_services}
- Total Requests: {total_requests:,}
- Services Without Fees: {services_without_fees}
- Current Total Revenue: {current_revenue:,.0f} QAR
- Active Scenario: {scenario_name}
""",
    
    "service_context": """
Service Details:
- Name: {service_name}
- Category: {category}
- Total Requests: {requests:,}
- Current Fee: {current_fee} QAR
- Annual Revenue: {revenue:,.0f} QAR
- Growth Rate: {growth_rate:.1f}%
""",
    
    "scenario_context": """
Scenario: {scenario_name}
- Services Modified: {num_services}
- Revenue Increase: {revenue_increase:,.0f} QAR ({revenue_pct:.1f}%)
- Total Revenue: {total_revenue:,.0f} QAR
"""
}

# Example prompts for users
EXAMPLE_QUESTIONS = {
    "en": [
        "Which services should I prioritize for adding fees?",
        "What's the best strategy to increase revenue by 20%?",
        "Explain the Pareto analysis chart",
        "What are the risks of adding 50 QAR to high-volume services?",
        "How can I implement fees without affecting demand significantly?"
    ],
    "ar": [
        "ما الخدمات التي يجب أن أعطيها الأولوية لإضافة رسوم؟",
        "ما أفضل استراتيجية لزيادة الإيرادات بنسبة 20٪؟",
        "اشرح مخطط تحليل باريتو",
        "ما مخاطر إضافة 50 ريال للخدمات عالية الحجم؟",
        "كيف يمكنني تطبيق رسوم دون التأثير على الطلب بشكل كبير؟"
    ]
}

# Insight generation prompts
INSIGHT_PROMPTS = {
    "executive_summary": """As a Senior Revenue Strategy Consultant for Qatar's Ministry of Labour, analyze this comprehensive service portfolio data:

PORTFOLIO OVERVIEW:
- Total Services: {total_services}
- Total Annual Requests: {total_requests:,}
- Services Without Fees: {services_without_fees} ({no_fee_pct:.1f}%)
- Current Annual Revenue: {current_revenue:,.0f} QAR
- Top Service by Volume: {top_service} ({top_requests:,} requests)

CRITICAL CONTEXT - DOCUMENTED SUGGESTIONS:
The operations team has provided specific, documented fee recommendations for 18+ services (33% of portfolio) with estimated untapped revenue of 83+ million QAR. These suggestions include:
- Per-person fees (عن كل شخص): e.g., 10 QAR per person for exit permits
- Per-month fees (عن كل شهر): e.g., 100 QAR per month for loan workers
- Tiered fees (لكل مهنة): Different rates for specialized vs non-specialized professions
- Conditional fees (في حال): e.g., 100 QAR only for private companies, not government
- Historical fee adjustments (كانت X تم تعديل الى Y): Previous fee changes provide elasticity insights

TOP 10 SERVICES BY REQUEST VOLUME:
{top_10_services}

YOUR TASK:
Generate 4-6 strategic insights in this EXACT format:

**STRUCTURE:**
1. Start with 3-4 bullet "Executive Summary" of key findings (one line each)
2. Then provide 4-6 detailed insights

**EACH INSIGHT MUST:**

1. **Reference ACTUAL documented suggestions** - Cite specific Arabic text and exact QAR amounts from operational data
2. **Prioritize by revenue impact** - Lead with highest-impact documented opportunities
3. **Assess implementation feasibility** - Distinguish employer-paid (low risk) vs employee-paid (politically sensitive)
4. **Recognize fee structure sophistication** - Note conditional pricing (gov't vs private), tiered rates, per-person/per-month structures
5. **Include assumption caveats** - When assuming durations or elasticity, explicitly state: "(Assumes X-month average duration - verify with historical data)" or "(Estimated Y% demand drop - monitor in pilot phase)"
6. **Use RELATIVE timeframes** - Say "Phase 1 (Months 1-3)", "Phase 2 (Months 4-6)", "Phase 3 (Months 7-12)" instead of specific quarters/years

**FORMAT FOR EACH INSIGHT:**
- Bold insight header (one sentence)
- 2-3 sentences with Arabic service name + English translation, exact QAR amounts, revenue calculation
- Risk assessment: "Demand elasticity: <5%" or "Political sensitivity: Medium"
- Action step: "RECOMMENDED ACTION: [specific next step with phase timing]"

**KEEP IT CONCISE:** 
- Executive summary: 4 bullets max
- Each detailed insight: 4-5 sentences max
- Total response: ~600-800 words

THINK LIKE: A consultant presenting slide deck to the Minister - start with executive summary, then supporting details.""",

    "opportunities": """As a GCC Public Sector Revenue Expert, analyze these documented revenue opportunities from Qatar Ministry of Labour operational data:

DOCUMENTED OPPORTUNITIES WITH ACTUAL SUGGESTIONS:
{opportunities_data}

CONTEXT: These are NOT hypothetical scenarios. These are REAL fee suggestions documented by the operations team in Arabic, including:
- Specific QAR amounts (e.g., "مئة ريال" = 100 QAR, "عشرة ريال" = 10 QAR)
- Fee structures (per-person "عن كل شخص", per-month "عن كل شهر", conditional "في حال")
- Special conditions (government vs private company pricing)
- Historical context where fees were previously changed

CRITICAL ANALYSIS FRAMEWORK:

1. **Service Type Matters**:
   - Employer-paid services (recruitment, work permits): LOW demand elasticity, HIGH implementation ease
   - Employee-paid services (license renewals): MEDIUM elasticity, requires careful messaging
   - Optional services (secondary employment, loan workers): HIGHER elasticity, monitor closely

2. **Qatar Labour Market Context**:
   - ~2M expatriate workers, ~350K active employers
   - Services tied to legal compliance = inelastic demand
   - Private sector services = cost-absorption capability
   - Government entity services = political sensitivity

3. **Documented Suggestion Quality**:
   - Operational teams understand service value and user willingness-to-pay
   - Conditional pricing (private vs government) shows sophisticated market understanding
   - Tiered pricing (specialized vs non-specialized professions) reflects cost-to-serve differences

YOUR TASK:
Generate strategic insights in this format:

**STRUCTURE:**
1. Start with 3-4 bullet executive summary highlighting top opportunities and total potential
2. Then provide 4-5 detailed insights

**EACH INSIGHT MUST:**

1. **Validate documented suggestions** - Reference specific Arabic text and explain why the suggested QAR amount is appropriate or needs adjustment
2. **Rank implementation sequence** - State which phase (Months 1-3, 4-6, 7-12) and why
3. **Include assumption caveats** - State any assumptions: "(Assumes X% demand elasticity - pilot test recommended)" or "(Assumes Y-month average - verify with operational data)"
4. **Assess specific risks** - State exact risk levels: "Demand elasticity: <5%" or "Political sensitivity: High (worker-paid fee)"
5. **Use relative timeframes** - "Phase 1 (Months 1-3): [action]" instead of specific dates
6. **Provide tactical milestones** - "Months 1-2: Stakeholder consultation. Months 3-4: System configuration. Month 5: Launch."

**FORMAT:**
- **Bold one-sentence insight header**
- Arabic service name (English translation): X requests × Y QAR = Z revenue
- Fee structure type and why it's smart/problematic
- Risk assessment with specific percentage or level
- RECOMMENDED ACTION: [Phase + specific tactical steps]

**KEEP IT CONCISE:**
- Executive summary: 3-4 bullets, one line each
- Each insight: 4-5 sentences maximum
- Total: ~600-800 words

**REVENUE CAVEAT:**
When projecting revenue for recurring fees (per-month, per-year), include caveat: "(Projected based on X-period average - actual revenue depends on duration patterns)"

Total Documented Potential: {total_potential:,.0f} QAR

THINK LIKE: Consultant validating operational team's proposals with expert analysis and phased implementation roadmap.""",

    "simulator": """A user is testing this fee change:

Service: {service_name}
Category: {category}
Current Fee: {current_fee} QAR
New Fee: {new_fee} QAR
Total Requests: {requests:,}
Revenue Impact: {revenue_increase:,.0f} QAR

Provide quick AI feedback:
1. Is this fee reasonable? (Compare to service value)
2. Demand elasticity concern level (High/Medium/Low)
3. Alternative fee amounts to consider
4. Risk assessment (1-2 sentences)
5. One sentence recommendation"""
}

# Report generation templates
REPORT_PROMPTS = {
    "executive_report": """Generate a comprehensive executive report for the Ministry of Labour leadership.

Data Summary:
{data_summary}

Scenario Analysis:
{scenario_info}

Structure the report with:

1. EXECUTIVE SUMMARY (2-3 paragraphs)
   - Current state overview
   - Key opportunity identified
   - Primary recommendation

2. CURRENT SITUATION ANALYSIS
   - Service portfolio overview
   - Revenue generation status
   - Growth trends and patterns
   - Gaps and opportunities

3. STRATEGIC RECOMMENDATIONS (Top 5)
   For each:
   - Specific action
   - Expected impact (with numbers)
   - Implementation difficulty
   - Timeline
   - Rationale

4. RISK ASSESSMENT
   - Demand response risks
   - Implementation challenges
   - Mitigation strategies

5. IMPLEMENTATION ROADMAP
   - Phase 1 (Immediate): 0-3 months
   - Phase 2 (Short-term): 3-6 months
   - Phase 3 (Long-term): 6-12 months

6. EXPECTED OUTCOMES
   - Revenue projections
   - Service quality impacts
   - Public response expectations

Use professional language, specific numbers, and be actionable."""
}

# Conversational scenario building
SCENARIO_BUILDING_PROMPTS = {
    "intent_parsing": """Parse this user request into a structured scenario:

User Request: "{user_input}"

Available services: {service_list}
Available categories: {category_list}

Extract and return JSON:
{{
  "intent_type": "add_fee" | "increase_revenue" | "category_pricing" | "custom",
  "services": ["list of service names"],
  "categories": ["list of categories"],
  "fee_amount": number or null,
  "constraints": {{
    "max_fee": number or null,
    "target_revenue": number or null,
    "percentage_increase": number or null
  }},
  "confidence": 0-1
}}

Be precise with service name matching (Arabic names included).""",

    "scenario_confirmation": """The user requested: "{user_input}"

I interpreted this as:
- Services: {services}
- Fee: {fee} QAR
- Expected Revenue Increase: {revenue_increase:,.0f} QAR

Is this correct? Generate a natural language confirmation message."""
}

