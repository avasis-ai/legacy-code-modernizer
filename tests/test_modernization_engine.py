"""Tests for Legacy Code Modernizer."""

import pytest
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from legacy_code_modernizer.modernization_engine import (
    ModernizationEngine,
    ModernizationConfig,
    SourceLanguage,
    TargetLanguage,
    ModernizationResult,
    ModernizationStatus,
    ASTNode,
    SourceCodeAnalysis,
    ASTParser,
    ASTMapper,
    CodeTranspiler
)


class TestSourceLanguage:
    """Tests for SourceLanguage enum."""
    
    def test_source_values(self):
        """Test source language values."""
        assert SourceLanguage.COBOL.value == "cobol"
        assert SourceLanguage.FORTRAN.value == "fortran"
        assert SourceLanguage.JAVA_LEGACY.value == "java_legacy"


class TestTargetLanguage:
    """Tests for TargetLanguage enum."""
    
    def test_target_values(self):
        """Test target language values."""
        assert TargetLanguage.GO.value == "go"
        assert TargetLanguage.RUST.value == "rust"
        assert TargetLanguage.TYPESCRIPT.value == "typescript"


class TestModernizationStatus:
    """Tests for ModernizationStatus enum."""
    
    def test_status_values(self):
        """Test status values."""
        assert ModernizationStatus.COMPLETE.value == "complete"
        assert ModernizationStatus.FAILED.value == "failed"
        assert ModernizationStatus.VALIDATING.value == "validating"


class TestModernizationConfig:
    """Tests for ModernizationConfig."""
    
    def test_config_creation(self):
        """Test creating a modernization config."""
        config = ModernizationConfig(
            source_language=SourceLanguage.JAVA_LEGACY,
            target_language=TargetLanguage.GO,
            preserve_comments=True,
            optimize_for_performance=True,
            include_tests=True,
            validation_strict=True
        )
        
        assert config.source_language == SourceLanguage.JAVA_LEGACY
        assert config.target_language == TargetLanguage.GO
        assert config.preserve_comments is True
    
    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = ModernizationConfig(
            source_language=SourceLanguage.FORTRAN,
            target_language=TargetLanguage.RUST,
            preserve_comments=True,
            optimize_for_performance=True,
            include_tests=False,
            validation_strict=True
        )
        
        data = config.to_dict()
        
        assert data['source_language'] == 'fortran'
        assert data['include_tests'] is False


class TestASTNode:
    """Tests for ASTNode."""
    
    def test_node_creation(self):
        """Test creating an AST node."""
        node = ASTNode(
            node_type="class",
            text="class Test {}",
            line=1,
            column=1,
            children=[],
            metadata={}
        )
        
        assert node.node_type == "class"
        assert node.text == "class Test {}"
    
    def test_node_to_dict(self):
        """Test converting node to dictionary."""
        node = ASTNode(
            node_type="method",
            text="public void test() {}",
            line=10,
            column=5,
            children=[],
            metadata={"complexity": 5}
        )
        
        data = node.to_dict()
        
        assert data['node_type'] == "method"
        assert data['line'] == 10


class TestSourceCodeAnalysis:
    """Tests for SourceCodeAnalysis."""
    
    def test_analysis_creation(self):
        """Test creating source analysis."""
        analysis = SourceCodeAnalysis(
            source_file="test.java",
            source_language=SourceLanguage.JAVA_LEGACY,
            total_lines=100,
            total_tokens=500,
            functions_found=[],
            classes_found=[],
            dependencies=[],
            complexity_score=5.0,
            analysis_timestamp=datetime.now()
        )
        
        assert analysis.source_file == "test.java"
        assert analysis.complexity_score == 5.0
    
    def test_analysis_to_dict(self):
        """Test converting analysis to dictionary."""
        analysis = SourceCodeAnalysis(
            source_file="test.java",
            source_language=SourceLanguage.JAVA_LEGACY,
            total_lines=100,
            total_tokens=500,
            functions_found=[{"name": "test", "line": 10}],
            classes_found=[{"name": "Test", "line": 1}],
            dependencies=["java.util"],
            complexity_score=5.0,
            analysis_timestamp=datetime.now()
        )
        
        data = analysis.to_dict()
        
        assert data['source_file'] == "test.java"
        assert len(data['functions_found']) == 1


class TestASTParser:
    """Tests for ASTParser."""
    
    def test_parse(self):
        """Test parsing source code."""
        source = "public class Test {}"
        
        ast = ASTParser.parse(source, SourceLanguage.JAVA_LEGACY)
        
        assert ast.node_type == "root"
        assert ast.metadata.get("line_count") > 0
        assert ast.metadata.get("token_count") > 0
    
    def test_analyze(self):
        """Test analyzing AST."""
        source = "public class Test {}"
        ast = ASTParser.parse(source, SourceLanguage.JAVA_LEGACY)
        
        analysis = ASTParser.analyze(ast, SourceLanguage.JAVA_LEGACY)
        
        assert analysis.source_language == SourceLanguage.JAVA_LEGACY
        assert analysis.total_lines > 0
        assert analysis.complexity_score > 0


class TestASTMapper:
    """Tests for ASTMapper."""
    
    def test_map_ast(self):
        """Test mapping AST to modern structure."""
        source = "public class Test {}"
        ast = ASTParser.parse(source, SourceLanguage.JAVA_LEGACY)
        
        mapped = ASTMapper.map_ast(ast, TargetLanguage.GO)
        
        assert mapped.node_type == "modern_root"
        assert mapped.metadata.get("target_language") == "go"


class TestCodeTranspiler:
    """Tests for CodeTranspiler."""
    
    def test_transpile_java_to_go(self):
        """Test transpiling Java to Go."""
        transpiler = CodeTranspiler()
        
        source = "public class Test {}"
        ast = ASTParser.parse(source, SourceLanguage.JAVA_LEGACY)
        mapped = ASTMapper.map_ast(ast, TargetLanguage.GO)
        
        code = transpiler.transpile(
            mapped,
            SourceLanguage.JAVA_LEGACY,
            TargetLanguage.GO
        )
        
        assert "package" in code.lower()
    
    def test_generate_test_coverage(self):
        """Test generating test coverage metrics."""
        transpiler = CodeTranspiler()
        
        coverage = transpiler.generate_test_coverage("test code")
        
        assert 'coverage_percent' in coverage
        assert 'test_count' in coverage


class TestModernizationEngine:
    """Tests for ModernizationEngine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = ModernizationEngine()
        
        assert engine._config is not None
        assert engine._job_counter == 0
        assert len(engine._results) == 0
    
    def test_modernize(self):
        """Test modernizing code."""
        engine = ModernizationEngine()
        
        config = ModernizationConfig(
            source_language=SourceLanguage.JAVA_LEGACY,
            target_language=TargetLanguage.GO,
            preserve_comments=True,
            optimize_for_performance=True,
            include_tests=True,
            validation_strict=True
        )
        
        result = engine.modernize("public class Test {}", config)
        
        assert result.job_id is not None
        assert result.status == ModernizationStatus.COMPLETE
        assert result.coverage_parity > 0
    
    def test_get_results(self):
        """Test getting results."""
        engine = ModernizationEngine()
        
        engine.modernize("test code", engine._config)
        
        results = engine.get_results()
        
        assert len(results) == 1
    
    def test_get_coverage_parity(self):
        """Test getting coverage parity."""
        engine = ModernizationEngine()
        
        engine.modernize("test code", engine._config)
        
        parity = engine.get_coverage_parity()
        
        assert 0.0 <= parity <= 1.0


class TestModernizationResult:
    """Tests for ModernizationResult."""
    
    def test_result_creation(self):
        """Test creating a modernization result."""
        result = ModernizationResult(
            job_id="MOD_001",
            source_file="test.java",
            source_language=SourceLanguage.JAVA_LEGACY,
            target_language=TargetLanguage.GO,
            modernized_code="// Modern code",
            status=ModernizationStatus.COMPLETE,
            errors=[],
            warnings=[],
            coverage_parity=0.95,
            complexity_comparison={
                "legacy_complexity": 10.0,
                "modern_complexity": 7.0,
                "improvement_percent": 30.0
            },
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        assert result.job_id == "MOD_001"
        assert result.coverage_parity == 0.95
    
    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        result = ModernizationResult(
            job_id="MOD_002",
            source_file="test.java",
            source_language=SourceLanguage.JAVA_LEGACY,
            target_language=TargetLanguage.RUST,
            modernized_code="// Modern code",
            status=ModernizationStatus.COMPLETE,
            errors=[],
            warnings=[],
            coverage_parity=0.90,
            complexity_comparison={
                "legacy_complexity": 15.0,
                "modern_complexity": 10.5,
                "improvement_percent": 30.0
            },
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        data = result.to_dict()
        
        assert data['job_id'] == "MOD_002"
        assert data['source_language'] == "java_legacy"
        assert data['coverage_parity'] == 0.90
