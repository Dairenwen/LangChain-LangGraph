# UML建模技术 — 考试复习完整指南
# UML Modeling Technology — Complete Exam Study Guide

> **基于教材**: *The Unified Modeling Language User Guide (2nd Edition)* by Grady Booch, James Rumbaugh, Ivar Jacobson  
> **涵盖章节**: 第1、2、4、5、6、8、9、10、11、12、13、15、16、17、18、19、20章

---

# Chapter 1: Why We Model / 第1章：为什么建模

---

### Q1: What is a model and what are its key characteristics?
### 什么是模型，它的关键特征是什么？

**EN:** A model is a **simplification of reality**. It provides the **blueprints of a system**. Models may encompass detailed plans as well as more general plans. A good model includes those elements that have broad effect and omits those minor elements that are not relevant to the given level of abstraction. Every system may be described from different aspects using different models, and each model is therefore a **semantically closed abstraction** of the system. A model may be **structural**, emphasizing the organization of the system, or it may be **behavioral**, emphasizing the dynamics of the system.

**CN:** 模型是**现实的简化**。它提供系统的**蓝图**。模型既可以包含详细的计划，也可以包含更概括的计划。一个好的模型包含那些具有广泛影响的元素，而省略那些与给定抽象层次无关的次要元素。每个系统都可以从不同方面用不同的模型来描述，因此每个模型都是系统的一个**语义封闭的抽象**。模型可以是**结构性的**（强调系统的组织），也可以是**行为性的**（强调系统的动态）。

---

### Q2: Why do we model? What is the fundamental reason?
### 我们为什么建模？根本原因是什么？

**EN:** We build models so that we can **better understand the system** we are developing. This is the one fundamental reason. We build models of complex systems because **we cannot comprehend such a system in its entirety**. Through modeling, we achieve four aims: (1) Models help us to **visualize** a system as it is or as we want it to be; (2) Models permit us to **specify** the structure or behavior of a system; (3) Models give us a template that guides us in **constructing** a system; (4) Models **document** the decisions we have made.

**CN:** 我们构建模型是为了**更好地理解我们正在开发的系统**——这是唯一根本的原因。我们为复杂系统构建模型，因为**我们无法完整地理解这样的系统**。通过建模，我们实现四个目标：(1) 模型帮助我们将系统**可视化**为当前或期望的样子；(2) 模型允许我们**规约**系统的结构或行为；(3) 模型为我们提供指导系统**构建**的模板；(4) 模型**记录**我们所做的决策。

---

### Q3: What are the four principles of modeling?
### 建模的四个原则是什么？

**EN:**
1. **The choice of what models to create has a profound influence on how a problem is attacked and how a solution is shaped.** The models you choose greatly affect how you view the problem and the solution.
2. **Every model may be expressed at different levels of precision.** The same model can be expressed at varying levels of detail depending on the audience and purpose.
3. **The best models are connected to reality.** Models should be grounded in the real world problem domain.
4. **No single model or view is sufficient. Every nontrivial system is best approached through a small set of nearly independent models with multiple viewpoints.** Multiple complementary views are needed to fully describe a complex system.

**CN:**
1. **选择创建什么模型对如何解决问题以及如何形成解决方案有着深远的影响。** 你选择的模型会极大地影响你看待问题和解决方案的方式。
2. **每个模型都可以用不同的精确度来表达。** 同一模型可以根据受众和目的以不同的详细程度表达。
3. **最好的模型是与现实相联系的。** 模型应该根植于真实世界的问题领域。
4. **没有单一的模型或视图是足够的。每个非平凡系统最好通过一组几乎独立的模型从多个视角来处理。** 需要多个互补的视图来全面描述一个复杂系统。

---

### Q4: What is the difference between the algorithmic perspective and the object-oriented perspective?
### 算法视角和面向对象视角有什么区别？

**EN:** The **algorithmic perspective** views software from the standpoint of algorithms and data structures, focusing on functions and the flow of data through those functions. However, this tends to yield **brittle systems** — as requirements change and the system grows, systems built with an algorithmic focus turn out to be very hard to maintain. The **object-oriented perspective** views software as a set of collaborating objects, each with its own state and behavior. The OO approach is decidedly part of the mainstream because it has proven to be of value in building systems in all sorts of problem domains, encompassing all degrees of size and complexity.

**CN:** **算法视角**从算法和数据结构的角度看待软件，关注函数以及数据在这些函数中的流动。然而，这往往会产生**脆弱的系统**——随着需求的变化和系统的增长，以算法为焦点构建的系统变得非常难以维护。**面向对象视角**将软件视为一组协作的对象，每个对象都有自己的状态和行为。面向对象方法已成为主流，因为它已被证明在各种问题领域构建系统时都很有价值，适用于各种规模和复杂度的系统。

---

### Q5: What is the purpose of the Unified Modeling Language?
### 统一建模语言的目的是什么？

**EN:** Visualizing, specifying, constructing, and documenting object-oriented systems is exactly the **purpose of the Unified Modeling Language**. A number of consequences flow from the choice of viewing the world in an OO fashion: What is the structure of a good OO architecture? What artifacts should the project create? Who should create them? How should they be measured? The UML addresses all of these.

**CN:** 可视化、规约、构建和文档化面向对象系统正是**统一建模语言的目的**。以面向对象方式看待世界会产生一系列后果：好的面向对象架构的结构是什么？项目应该创建哪些制品？谁应该创建它们？如何衡量它们？UML 解决了所有这些问题。

---

# Chapter 2: Introducing the UML / 第2章：UML简介

---

### Q6: What is the UML? Describe its four key aspects.
### 什么是UML？描述其四个关键方面。

**EN:** The UML is a language for **Visualizing**, **Specifying**, **Constructing**, and **Documenting** the artifacts of a software-intensive system.

**CN:** UML 是一种用于**可视化**、**规约**、**构建**和**文档化**软件密集型系统制品的语言。

---

### Q7: Why is the UML a language for visualizing?
### 为什么UML是一种用于可视化的语言？

**EN:** For many programmers, the distance between thinking of an implementation and then pounding it out in code is close to zero. However, there are problems: (1) Communicating conceptual models to others is error-prone unless everyone speaks the same language; (2) Some things about a software system can't be understood unless you build models that transcend textual programming languages; (3) If the developer never wrote down the models in his head, that information would be lost forever once that developer moved on. The UML addresses the third issue — an explicit model facilitates communication. Behind each symbol in the UML notation is a **well-defined semantics**, so one developer can write a UML model and another developer, or even another tool, can interpret it unambiguously.

**CN:** 对许多程序员来说，从思考实现到敲出代码之间的距离接近于零。然而，存在以下问题：(1) 除非每个人都使用相同的语言，否则将概念模型传达给他人容易出错；(2) 软件系统的某些方面，除非你构建超越文本编程语言的模型，否则无法理解；(3) 如果编写代码的开发者从未记录下他脑海中的模型，那么一旦该开发者离开，这些信息将永远丢失。UML 解决了第三个问题——显式模型促进了沟通。UML 符号中每个符号背后都有**明确定义的语义**，因此一个开发者可以编写 UML 模型，而另一个开发者，甚至是另一个工具，都可以无歧义地解释它。

---

### Q8: What does it mean that the UML is a language for specifying?
### UML作为规约语言意味着什么？

**EN:** Specifying means building models that are **precise, unambiguous, and complete**. The UML addresses the specification of all the important **analysis, design, and implementation decisions** that must be made in developing and deploying a software-intensive system.

**CN:** 规约意味着构建**精确、无歧义和完整**的模型。UML 处理在开发和部署软件密集型系统过程中必须做出的所有重要的**分析、设计和实现决策**的规约。

---

### Q9: What does it mean that the UML is a language for constructing?
### UML作为构建语言意味着什么？

**EN:** The UML is not a visual programming language, but its models can be directly connected to a variety of programming languages. This mapping permits **forward engineering** — the generation of code from a UML model into a programming language. The reverse is also possible: you can reconstruct a model from an implementation back into the UML (**reverse engineering**).

**CN:** UML 不是一种可视化编程语言，但它的模型可以直接连接到各种编程语言。这种映射允许**正向工程**——从 UML 模型生成代码到编程语言。反过来也是可能的：你可以从实现重建模型回到 UML（**逆向工程**）。

