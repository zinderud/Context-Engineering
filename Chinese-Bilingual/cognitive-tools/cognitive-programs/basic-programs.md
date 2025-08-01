# Basic Cognitive Programs  基本认知程序

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#basic-cognitive-programs)

> "Programs must be written for people to read, and only incidentally for machines to execute." — Harold Abelson  
> “程序必须写出来供人阅读，而仅仅偶尔供机器执行。”——哈罗德·阿贝尔森

## Overview  概述

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#overview)

Cognitive programs are structured, reusable prompt patterns that guide language models through specific reasoning processes. Unlike traditional templates, cognitive programs incorporate programming concepts such as variables, functions, control structures, and composition to create more sophisticated and adaptable reasoning frameworks.  
认知程序是结构化的、可重复使用的提示模式，用于引导语言模型完成特定的推理过程。与传统模板不同，认知程序融合了变量、函数、控制结构和组合等编程概念，从而创建更复杂、适应性更强的推理框架。

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  COGNITIVE PROGRAM STRUCTURE                                 │
│                                                              │
│  function programName(parameters) {                          │
│    // Processing logic                                       │
│    return promptText;                                        │
│  }                                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Fundamental Programming Concepts  
基本编程概念

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#fundamental-programming-concepts)

### 1. Functions and Parameters  
1.功能与参数

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#1-functions-and-parameters)

The basic building block of cognitive programs is the function with parameters.  
认知程序的基本构建块是带有参数的函数。

```js
function analyze(topic, depth="detailed", focus=null) {
  // Function implementation
  let depthInstructions = {
    "brief": "Provide a high-level overview with 1-2 key points.",
    "detailed": "Explore major aspects with supporting evidence.",
    "comprehensive": "Conduct an exhaustive analysis with nuanced considerations."
  };
  
  let focusInstruction = focus ? 
    `Focus particularly on aspects related to ${focus}.` : 
    "Cover all relevant aspects evenly.";
  
  return `
    Task: Analyze ${topic} at a ${depth} level.
    
    Instructions:
    ${depthInstructions[depth]}
    ${focusInstruction}
    
    Please structure your analysis with clear headings and bullet points where appropriate.
  `;
}
```

**Key Components**:  
**关键组件** ：

- **Function Name**: Describes the cognitive operation (e.g., `analyze`)  
    **函数名称** ：描述认知操作（例如， `analyze` ）
- **Parameters**: Customize the operation (e.g., topic, depth, focus)  
    **参数** ：自定义操作（例如主题、深度、焦点）
- **Default Values**: Provide sensible defaults that can be overridden  
    **默认值** ：提供可以覆盖的合理默认值
- **Return Value**: The complete prompt to be sent to the LLM  
    **返回值** ：发送给 LLM 的完整提示

**Usage Example**:  
**使用示例** ：

```js
// Generate prompts with different parameter combinations
const climatePrompt = analyze("climate change", "detailed", "economic impacts");
const aiPrompt = analyze("artificial intelligence", "comprehensive");
const quickCovidPrompt = analyze("COVID-19", "brief");
```

### 2. Conditional Logic  2.条件逻辑

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#2-conditional-logic)

Conditional statements allow cognitive programs to adapt based on inputs or context.  
条件语句允许认知程序根据输入或上下文进行调整。

```js
function solve_problem(problem, show_work=true, difficulty=null) {
  // Detect problem type and difficulty if not specified
  let problemType = detect_problem_type(problem);
  let problemDifficulty = difficulty || estimate_difficulty(problem);
  
  // Determine appropriate approach based on problem type
  let approach;
  let steps;
  
  if (problemType === "mathematical") {
    approach = "mathematical";
    steps = [
      "Identify the variables and given information",
      "Determine the appropriate formulas or techniques",
      "Apply the formulas step-by-step",
      "Verify the solution"
    ];
  } else if (problemType === "logical") {
    approach = "logical reasoning";
    steps = [
      "Identify the logical structure of the problem",
      "Determine the key premises and conclusions",
      "Apply logical inference rules",
      "Verify the argument validity"
    ];
  } else {
    approach = "analytical";
    steps = [
      "Break down the problem into components",
      "Analyze each component systematically",
      "Synthesize insights to form a solution",
      "Verify the solution addresses the original problem"
    ];
  }
  
  // Adjust detail level based on difficulty
  let detailLevel;
  if (problemDifficulty === "basic") {
    detailLevel = "Provide straightforward explanations suitable for beginners.";
  } else if (problemDifficulty === "intermediate") {
    detailLevel = "Include relevant concepts and techniques with clear explanations.";
  } else {
    detailLevel = "Provide detailed explanations and consider edge cases or alternative approaches.";
  }
  
  // Construct the prompt
  return `
    Task: Solve the following ${approach} problem.
    
    Problem: ${problem}
    
    ${show_work ? "Show your work using these steps:" : "Provide the solution:"}
    ${show_work ? steps.map((step, i) => `${i+1}. ${step}`).join("\n") : ""}
    
    ${detailLevel}
    
    ${show_work ? "Conclude with a clear final answer." : ""}
  `;
}

// Helper functions (simplified for illustration)
function detect_problem_type(problem) {
  // In a real implementation, this would use heuristics or LLM classification
  if (problem.includes("calculate") || problem.includes("equation")) {
    return "mathematical";
  } else if (problem.includes("valid") || problem.includes("argument")) {
    return "logical";
  } else {
    return "general";
  }
}

function estimate_difficulty(problem) {
  // Simplified difficulty estimation
  const wordCount = problem.split(" ").length;
  if (wordCount < 20) return "basic";
  if (wordCount < 50) return "intermediate";
  return "advanced";
}
```

**Key Components**:  
**关键组件** ：

- **Condition Checks**: Branch based on problem characteristics  
    **条件检查** ：根据问题特征进行分支
- **Variable Assignment**: Set values based on conditions  
    **变量赋值** ：根据条件设置值
- **Dynamic Content**: Build different prompts based on conditions  
    **动态内容** ：根据条件构建不同的提示

**Usage Example**:  
**使用示例** ：

```js
// Generate prompts for different problem types
const mathPrompt = solve_problem("Solve for x in the equation 2x + 5 = 17");
const logicPrompt = solve_problem("Determine if the following argument is valid...", true, "advanced");
```

### 3. Loops and Iteration  3.循环和迭代

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#3-loops-and-iteration)

Loops allow for repeated operations or building complex structures.  
循环允许重复操作或构建复杂的结构。

```js
function multi_perspective_analysis(topic, perspectives=["economic", "social", "political"], depth="detailed") {
  // Base prompt
  let prompt = `
    Task: Analyze ${topic} from multiple perspectives.
    
    Instructions:
    Please provide a ${depth} analysis of ${topic} from each of the following perspectives.
  `;
  
  // Add sections for each perspective
  for (let i = 0; i < perspectives.length; i++) {
    const perspective = perspectives[i];
    prompt += `
    
    Perspective ${i+1}: ${perspective.charAt(0).toUpperCase() + perspective.slice(1)}
    - Analyze ${topic} through a ${perspective} lens
    - Identify key ${perspective} factors and implications
    - Consider important ${perspective} stakeholders and their interests
    `;
  }
  
  // Add integration section
  prompt += `
  
  Integration:
  After analyzing from these individual perspectives, synthesize the insights to provide a holistic understanding of ${topic}.
  Identify areas of alignment and tension between different perspectives.
  
  Conclusion:
  Summarize the most significant insights from this multi-perspective analysis.
  `;
  
  return prompt;
}
```

**Key Components**:  
**关键组件** ：

- **Loop Construction**: Iterate through a collection (e.g., perspectives)  
    **循环构造** ：遍历集合（例如视角）
- **Content Accumulation**: Build up prompt content incrementally  
    **内容积累** ：逐步积累提示内容
- **Dynamic Generation**: Create variable numbers of sections based on inputs  
    **动态生成** ：根据输入创建可变数量的部分

**Usage Example**:  
**使用示例** ：

```js
// Standard perspectives
const climatePrompt = multi_perspective_analysis("climate change");

// Custom perspectives
const aiPrompt = multi_perspective_analysis(
  "artificial intelligence ethics",
  ["technological", "ethical", "regulatory", "business"]
);
```

### 4. Function Composition  4. 函数组合

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#4-function-composition)

Function composition enables building complex cognitive programs from simpler ones.  
函数组合使得能够从简单的认知程序构建复杂的认知程序。

```js
function research_and_analyze(topic, research_depth="comprehensive", analysis_type="cause-effect") {
  // First, generate a research prompt
  const researchPrompt = research(topic, research_depth);
  
  // Then, set up the analysis to use the research results
  return `
    First, conduct research on ${topic}:
    
    ${researchPrompt}
    
    After completing the research above, analyze your findings using this framework:
    
    ${analyze(topic, "detailed", analysis_type)}
    
    Finally, synthesize your research and analysis into a coherent conclusion that addresses the most significant aspects of ${topic}.
  `;
}

// Component functions
function research(topic, depth="comprehensive") {
  const depthInstructions = {
    "brief": "Identify 3-5 key facts about",
    "standard": "Research the main aspects of",
    "comprehensive": "Conduct in-depth research on all significant dimensions of"
  };
  
  return `
    Task: ${depthInstructions[depth]} ${topic}.
    
    Instructions:
    - Identify credible information sources
    - Extract relevant facts, statistics, and expert opinions
    - Organize findings by subtopic
    - Note areas of consensus and disagreement
    
    Present your research in a structured format with clear headings and bullet points.
  `;
}

function analyze(topic, depth="detailed", framework="general") {
  const frameworkInstructions = {
    "general": "Analyze the key aspects and implications of",
    "cause-effect": "Analyze the causes and effects related to",
    "compare-contrast": "Compare and contrast different perspectives on",
    "swot": "Conduct a SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis of"
  };
  
  return `
    Task: ${frameworkInstructions[framework]} ${topic}.
    
    Instructions:
    - Apply the ${framework} analytical framework
    - Support analysis with evidence from reliable sources
    - Consider multiple viewpoints and potential biases
    - Identify the most significant insights
    
    Structure your analysis logically with clear sections and supporting points.
  `;
}
```

**Key Components**:  
**关键组件** ：

- **Function Calls**: Using one function inside another  
    **函数调用** ：在一个函数内部使用另一个函数
- **Result Integration**: Combining outputs from multiple functions  
    **结果集成** ：组合多个函数的输出
- **Modular Design**: Building complex operations from simpler ones  
    **模块化设计** ：从简单的操作构建复杂的操作

**Usage Example**:  
**使用示例** ：

```js
// Combined research and analysis prompts
const climatePrompt = research_and_analyze("climate change mitigation strategies", "comprehensive", "swot");
const aiPrompt = research_and_analyze("artificial intelligence regulation", "standard", "compare-contrast");
```

## Basic Cognitive Program Templates  
基本认知程序模板

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#basic-cognitive-program-templates)

### 1. Problem Solver Program  
1. 问题解决程序

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#1-problem-solver-program)

A comprehensive program for solving structured problems.  
解决结构化问题的综合程序。

```js
function problem_solver(problem, options = {}) {
  // Default options
  const defaults = {
    show_work: true,
    verify_solution: true,
    approach: "auto-detect", // Can be "auto-detect", "mathematical", "logical", "conceptual"
    detail_level: "standard" // Can be "brief", "standard", "detailed"
  };
  
  // Merge defaults with provided options
  const settings = {...defaults, ...options};
  
  // Determine approach if auto-detect
  let approach = settings.approach;
  if (approach === "auto-detect") {
    // Simple heuristic detection (would be more sophisticated in practice)
    if (/\d[+\-*/=]/.test(problem) || /equation|calculate|solve for|find the value/.test(problem.toLowerCase())) {
      approach = "mathematical";
    } else if (/valid|argument|fallacy|premise|conclusion/.test(problem.toLowerCase())) {
      approach = "logical";
    } else {
      approach = "conceptual";
    }
  }
  
  // Build approach-specific instructions
  let approachInstructions;
  if (approach === "mathematical") {
    approachInstructions = `
      Mathematical Problem Solving Approach:
      1. Identify all variables, constants, and their relationships
      2. Determine the appropriate mathematical techniques or formulas
      3. Apply the techniques systematically
      4. Compute the solution with careful attention to units and precision
    `;
  } else if (approach === "logical") {
    approachInstructions = `
      Logical Reasoning Approach:
      5. Identify the logical structure, premises, and conclusions
      6. Determine the type of logical argument being made
      7. Apply appropriate rules of inference
      8. Evaluate the validity and soundness of the argument
    `;
  } else {
    approachInstructions = `
      Conceptual Analysis Approach:
      9. Clarify key concepts and their relationships
      10. Break down the problem into manageable components
      11. Analyze each component systematically
      12. Synthesize insights to form a comprehensive solution
    `;
  }
  
  // Adjust detail level
  let detailInstructions;
  if (settings.detail_level === "brief") {
    detailInstructions = "Provide a concise solution focusing on the key steps and insights.";
  } else if (settings.detail_level === "standard") {
    detailInstructions = "Provide a clear explanation of your reasoning process with sufficient detail.";
  } else {
    detailInstructions = "Provide a thorough explanation with detailed reasoning at each step.";
  }
  
  // Build verification section if requested
  let verificationSection = "";
  if (settings.verify_solution) {
    verificationSection = `
      Verification:
      After completing your solution, verify its correctness by:
      13. Checking that it directly addresses the original problem
      14. Testing the solution with specific examples or edge cases if applicable
      15. Reviewing calculations or logical steps for errors
      16. Confirming that all constraints and conditions are satisfied
    `;
  }
  
  // Construct the final prompt
  return `
    Task: Solve the following problem.
    
    Problem: ${problem}
    
    ${settings.show_work ? "Please show your complete work and reasoning process." : "Provide your solution."}
    
    ${approachInstructions}
    
    ${detailInstructions}
    
    ${verificationSection}
    
    Conclusion:
    End with a clear, direct answer to the original problem.
  `;
}
```

**Usage Example**:  
**使用示例** ：

```js
// Mathematical problem with verification
const mathPrompt = problem_solver(
  "If a train travels at 60 mph for 2.5 hours, how far does it go?",
  { approach: "mathematical", verify_solution: true }
);

// Logical problem with brief explanation
const logicPrompt = problem_solver(
  "If all A are B, and some B are C, can we conclude that some A are C?",
  { approach: "logical", detail_level: "brief" }
);

// Conceptual problem with detailed explanation
const conceptPrompt = problem_solver(
  "What are the ethical implications of autonomous vehicles making life-or-death decisions?",
  { approach: "conceptual", detail_level: "detailed" }
);
```

### 2. Step-by-Step Reasoning Program  
2. 逐步推理程序

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#2-step-by-step-reasoning-program)

A program that guides through explicit reasoning steps.  
指导明确推理步骤的程序。

```js
function step_by_step_reasoning(problem, steps = null, options = {}) {
  // Default options
  const defaults = {
    explanations: true, // Include explanations for each step
    examples: false,    // Include examples in the instructions
    difficulty: "auto"  // Can be "auto", "basic", "intermediate", "advanced"
  };
  
  // Merge defaults with provided options
  const settings = {...defaults, ...options};
  
  // Determine difficulty if auto
  let difficulty = settings.difficulty;
  if (difficulty === "auto") {
    // Simple heuristic (would be more sophisticated in practice)
    const wordCount = problem.split(" ").length;
    const complexityIndicators = ["complex", "challenging", "difficult", "advanced"];
    
    const hasComplexityMarkers = complexityIndicators.some(indicator => 
      problem.toLowerCase().includes(indicator)
    );
    
    if (hasComplexityMarkers || wordCount > 50) {
      difficulty = "advanced";
    } else if (wordCount > 25) {
      difficulty = "intermediate";
    } else {
      difficulty = "basic";
    }
  }
  
  // Default steps if not provided
  if (!steps) {
    steps = [
      { id: "understand", name: "Understand the Problem", 
        description: "Carefully read the problem and identify what is being asked." },
      { id: "analyze", name: "Analyze Given Information", 
        description: "Identify all relevant information provided in the problem." },
      { id: "plan", name: "Plan a Solution Approach", 
        description: "Determine a strategy or method to solve the problem." },
      { id: "execute", name: "Execute the Plan", 
        description: "Carry out your solution plan step by step." },
      { id: "verify", name: "Verify the Solution", 
        description: "Check that your answer correctly solves the original problem." }
    ];
  }
  
  // Adjust explanation detail based on difficulty
  let explanationPrompt;
  if (difficulty === "basic") {
    explanationPrompt = "Explain your thinking using simple, clear language.";
  } else if (difficulty === "intermediate") {
    explanationPrompt = "Provide thorough explanations that connect concepts and steps.";
  } else {
    explanationPrompt = "Include detailed explanations that address nuances and potential alternative approaches.";
  }
  
  // Build examples section if requested
  let examplesSection = "";
  if (settings.examples) {
    examplesSection = `
      Example of Step-by-Step Reasoning:
      
      Problem: What is the area of a rectangle with length 8m and width 5m?
      
      Step 1: Understand the Problem
      I need to find the area of a rectangle with given dimensions.
      
      Step 2: Analyze Given Information
      - Length = 8 meters
      - Width = 5 meters
      
      Step 3: Plan a Solution Approach
      I'll use the formula: Area of rectangle = length × width
      
      Step 4: Execute the Plan
      Area = 8m × 5m = 40 square meters
      
      Step 5: Verify the Solution
      I can verify by dividing the area by the width: 40 ÷ 5 = 8, which equals the length.
      
      Final Answer: The area of the rectangle is 40 square meters.
    `;
  }
  
  // Build the steps instructions
  let stepsInstructions = "";
  steps.forEach((step, index) => {
    stepsInstructions += `
      Step ${index + 1}: ${step.name}
      ${step.description}
      ${settings.explanations ? `For this step: ${explanationPrompt}` : ""}
    `;
  });
  
  // Construct the final prompt
  return `
    Task: Solve the following problem using a step-by-step reasoning approach.
    
    Problem: ${problem}
    
    Instructions:
    Break down your solution into the following steps, showing your work clearly at each stage.
    
    ${stepsInstructions}
    
    Conclusion:
    After completing all steps, provide your final answer clearly.
    
    ${examplesSection}
  `;
}
```

**Usage Example**:  
**使用示例** ：

```js
// Basic problem with standard steps
const basicPrompt = step_by_step_reasoning(
  "A car travels 150 miles in 3 hours. What is its average speed?",
  null,
  { difficulty: "basic", examples: true }
);

// Custom steps for a specific reasoning approach
const customSteps = [
  { id: "identify", name: "Identify Variables", 
    description: "List all variables in the problem." },
  { id: "formula", name: "Select Formula", 
    description: "Choose the appropriate formula for this problem." },
  { id: "substitute", name: "Substitute Values", 
    description: "Plug the known values into the formula." },
  { id: "solve", name: "Solve Equation", 
    description: "Solve for the unknown variable." },
  { id: "check", name: "Check Solution", 
    description: "Verify your answer makes sense." }
];

const physicsPrompt = step_by_step_reasoning(
  "An object is thrown upward with an initial velocity of 15 m/s. How high will it go?",
  customSteps,
  { difficulty: "intermediate" }
);
```

### 3. Comparative Analysis Program  
3. 比较分析程序

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#3-comparative-analysis-program)

A program for structured comparison between multiple items.  
用于对多个项目进行结构化比较的程序。

```js
function comparative_analysis(items, criteria = null, options = {}) {
  // Default options
  const defaults = {
    format: "table",       // Can be "table", "narrative", "pros-cons"
    conclusion: true,      // Include a conclusion section
    highlight_differences: true, // Emphasize key differences
    detail_level: "balanced" // Can be "brief", "balanced", "detailed"
  };
  
  // Merge defaults with provided options
  const settings = {...defaults, ...options};
  
  // Ensure items is an array
  const itemsList = Array.isArray(items) ? items : [items];
  
  // Generate default criteria if none provided
  if (!criteria) {
    criteria = [
      { id: "features", name: "Key Features" },
      { id: "advantages", name: "Advantages" },
      { id: "limitations", name: "Limitations" },
      { id: "applications", name: "Applications" }
    ];
  }
  
  // Format items for display
  const itemsDisplay = itemsList.join(", ");
  
  // Build criteria section
  let criteriaSection = "";
  criteria.forEach((criterion, index) => {
    criteriaSection += `
      ${index + 1}. ${criterion.name}${criterion.description ? `: ${criterion.description}` : ""}
    `;
  });
  
  // Build format-specific instructions
  let formatInstructions;
  if (settings.format === "table") {
    formatInstructions = `
      Present your analysis in a table format:
      
      | Criteria | ${itemsList.map(item => item).join(" | ")} |
      |----------|${itemsList.map(() => "---------").join("|")}|
      ${criteria.map(c => `| ${c.name} | ${itemsList.map(() => "?").join(" | ")} |`).join("\n")}
      
      For each cell, provide a concise analysis of how the item performs on that criterion.
    `;
  } else if (settings.format === "pros-cons") {
    formatInstructions = `
      For each item, provide a structured pros and cons analysis:
      
      ${itemsList.map(item => `
      ## ${item}
      
      Pros:
      - [Pro point 1]
      - [Pro point 2]
      
      Cons:
      - [Con point 1]
      - [Con point 2]
      `).join("\n")}
      
      Ensure that your pros and cons directly address the criteria.
    `;
  } else {
    formatInstructions = `
      Present your analysis in a narrative format:
      
      For each criterion, discuss how all items compare, highlighting similarities and differences.
      
      ${criteria.map(c => `## ${c.name}\n[Comparative analysis for this criterion]`).join("\n\n")}
    `;
  }
  
  // Build detail level instructions
  let detailInstructions;
  if (settings.detail_level === "brief") {
    detailInstructions = "Focus on the most essential points for each criterion, keeping the analysis concise.";
  } else if (settings.detail_level === "balanced") {
    detailInstructions = "Provide a balanced analysis with sufficient detail to support meaningful comparison.";
  } else {
    detailInstructions = "Include comprehensive details for each criterion, exploring nuances and edge cases.";
  }
  
  // Build differences section if requested
  let differencesSection = "";
  if (settings.highlight_differences) {
    differencesSection = `
      Key Differences:
      After completing your comparative analysis, highlight the most significant differences between the items.
      Focus on differences that would be most relevant for decision-making purposes.
    `;
  }
  
  // Build conclusion section if requested
  let conclusionSection = "";
  if (settings.conclusion) {
    conclusionSection = `
      Conclusion:
      Synthesize your analysis into a conclusion that summarizes the comparison.
      Avoid simplistic "X is better than Y" statements unless clearly supported by the analysis.
      Instead, clarify the contexts or scenarios in which each item might be preferred.
    `;
  }
  
  // Construct the final prompt
  return `
    Task: Conduct a comparative analysis of the following items: ${itemsDisplay}.
    
    Instructions:
    Compare these items across the following criteria:
    ${criteriaSection}
    
    ${detailInstructions}
    
    ${formatInstructions}
    
    ${differencesSection}
    
    ${conclusionSection}
  `;
}
```

**Usage Example**:  
**使用示例** ：

```js
// Simple comparison with default criteria
const phonePrompt = comparative_analysis(
  ["iPhone 14", "Samsung Galaxy S23", "Google Pixel 7"],
  null,
  { format: "table" }
);

// Custom criteria with narrative format
const customCriteria = [
  { id: "efficacy", name: "Efficacy", description: "How effective is the treatment?" },
  { id: "side_effects", name: "Side Effects", description: "What are the common side effects?" },
  { id: "cost", name: "Cost", description: "What is the typical cost?" },
  { id: "accessibility", name: "Accessibility", description: "How accessible is the treatment?" }
];

const treatmentPrompt = comparative_analysis(
  ["Cognitive Behavioral Therapy", "Medication", "Mindfulness-Based Stress Reduction"],
  customCriteria,
  { format: "narrative", detail_level: "detailed" }
);
```

## Implementing Cognitive Programs  
实施认知程序

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#implementing-cognitive-programs)

In practical applications, cognitive programs can be implemented in various ways:  
在实际应用中，认知程序可以通过多种方式实现：

### 1. JavaScript/TypeScript Implementation  
1. JavaScript/TypeScript 实现

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#1-javascripttypescript-implementation)

```js
// In a Node.js or browser environment
const cognitivePrograms = {
  problemSolver: function(problem, options = {}) {
    // Implementation as shown above
  },
  
  stepByStepReasoning: function(problem, steps = null, options = {}) {
    // Implementation as shown above
  },
  
  // Add more programs as needed
};

// Usage
const prompt = cognitivePrograms.problemSolver("Solve for x: 2x + 5 = 15");
callLLM(prompt).then(response => console.log(response));
```

### 2. Python Implementation  2. Python 实现

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#2-python-implementation)

```python
class CognitivePrograms:
    @staticmethod
    def problem_solver(problem, **options):
        # Implementation converted to Python
        defaults = {
            "show_work": True,
            "verify_solution": True,
            "approach": "auto-detect",
            "detail_level": "standard"
        }
        
        # Merge defaults with provided options
        settings = {**defaults, **options}
        
        # Rest of implementation...
        return prompt
    
    @staticmethod
    def step_by_step_reasoning(problem, steps=None, **options):
        # Implementation converted to Python
        pass
    
    # Add more programs as needed

# Usage
prompt = CognitivePrograms.problem_solver("Solve for x: 2x + 5 = 15")
response = call_llm(prompt)
print(response)
```

### 3. Prompt String Templates  
3. 提示字符串模板

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#3-prompt-string-templates)

For simpler implementations without a programming environment:  
对于没有编程环境的更简单的实现：

```
PROBLEM SOLVER TEMPLATE

Task: Solve the following problem.

Problem: {{PROBLEM}}

Please show your complete work and reasoning process.

{{APPROACH_INSTRUCTIONS}}

{{DETAIL_INSTRUCTIONS}}

{{VERIFICATION_SECTION}}

Conclusion:
End with a clear, direct answer to the original problem.
```

## Measurement and Optimization  
测量与优化

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#measurement-and-optimization)

When using cognitive programs, measure their effectiveness by:  
使用认知程序时，通过以下方式衡量其有效性：

1. **Accuracy**: Does the program consistently lead to correct solutions?  
    **准确性** ：程序是否始终能够得出正确的解决方案？
2. **Token Efficiency**: What is the token overhead compared to simpler prompts?  
    **令牌效率** ：与更简单的提示相比，令牌开销是多少？
3. **Adaptability**: How well does the program handle different variations of problems?  
    **适应性** ：该程序如何处理不同类型的问题？
4. **Clarity**: Is the reasoning process clear and easy to follow?  
    **清晰度** ：推理过程是否清晰且易于理解？

Optimize your programs by:  
通过以下方式优化您的程序：

- Removing unnecessary instructions that don't improve performance  
    删除不会提高性能的不必要指令
- Adjusting parameters based on empirical testing  
    根据实证检验调整参数
- Creating specialized variants for different problem domains  
    为不同的问题领域创建专门的变体

## Next Steps  后续步骤

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#next-steps)

- Explore [advanced-programs.md](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/advanced-programs.md) for more sophisticated programming patterns  
    探索 [advanced-programs.md](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/advanced-programs.md) 以获得更复杂的编程模式
- See [program-library.py](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/program-library.py) for a complete implementation library  
    完整的实现库请参见 [program-library.py](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/program-library.py)
- Try [program-examples.ipynb](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/program-examples.ipynb) for interactive examples and experiments  
    尝试 [program-examples.ipynb](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/program-examples.ipynb) 获取交互式示例和实验

---

## Deeper Dive: Cognitive Program Design Principles  
深入探讨：认知程序设计原则

[](https://github.com/KashiwaByte/Context-Engineering-Chinese-Bilingual/blob/main/Chinese-Bilingual/cognitive-tools/cognitive-programs/basic-programs.md#deeper-dive-cognitive-program-design-principles)

When designing your own cognitive programs, consider these principles:  
在设计自己的认知程序时，请考虑以下原则：

1. **Single Responsibility**: Each program should focus on one type of cognitive operation  
    **单一职责** ：每个程序应该专注于一种认知操作
2. **Clear Parameters**: Make customization options explicit and well-documented  
    **清晰的参数** ：使自定义选项明确且有据可查
3. **Sensible Defaults**: Provide reasonable default values for optional parameters  
    **合理的默认值** ：为可选参数提供合理的默认值
4. **Error Handling**: Consider how the program should behave with unexpected inputs  
    **错误处理** ：考虑程序在遇到意外输入时应该如何处理
5. **Composability**: Design programs that can be easily combined with others  
    **可组合性** ：设计可以轻松与其他程序组合的程序
6. **Testability**: Make it easy to evaluate the program's effectiveness  
    **可测试性** ：可以轻松评估程序的有效性

These principles help create cognitive programs that are reusable, maintainable, and effective across a wide range of applications.  
这些原则有助于创建可在广泛应用中重复使用、可维护且有效的认知程序。