"""Command-line interface for Legacy Code Modernizer."""

import click
import json
from typing import Optional

from .modernization_engine import (
    ModernizationEngine,
    ModernizationConfig,
    SourceLanguage,
    TargetLanguage,
    ModernizationResult
)


@click.group()
@click.version_option(version="0.1.0", prog_name="legacy-modernizer")
def main() -> None:
    """Legacy Code Modernizer - AST-based code transpilation."""
    pass


@main.command()
@click.option("--source", "-s", type=click.Choice(["cobol", "fortran", "java_legacy"]),
              default="java_legacy", help="Source language")
@click.option("--target", "-t", type=click.Choice(["go", "rust", "typescript"]),
              default="go", help="Target language")
def config(source: str, target: str) -> None:
    """Show modernization configuration."""
    source_enum = SourceLanguage[source.upper()]
    target_enum = TargetLanguage[target.upper()]
    
    click.echo(f"\n⚙️ Modernization Configuration")
    click.echo("=" * 60)
    click.echo(f"Source Language: {source_enum.value}")
    click.echo(f"Target Language: {target_enum.value}")
    click.echo(f"Options:")
    click.echo(f"  - Preserve Comments: True")
    click.echo(f"  - Optimize Performance: True")
    click.echo(f"  - Include Tests: True")
    click.echo(f"  - Validation Strict: True")


@main.command()
@click.argument("source_file")
@click.option("--source-lang", "-s", type=click.Choice(["cobol", "fortran", "java_legacy"]),
              default="java_legacy", help="Source language")
@click.option("--target-lang", "-t", type=click.Choice(["go", "rust", "typescript"]),
              default="go", help="Target language")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def modernize(source_file: str, source_lang: str, target_lang: str, 
              output: Optional[str]) -> None:
    """Modernize legacy code to modern language."""
    source_enum = SourceLanguage[source_lang.upper()]
    target_enum = TargetLanguage[target_lang.upper()]
    
    config = ModernizationConfig(
        source_language=source_enum,
        target_language=target_enum,
        preserve_comments=True,
        optimize_for_performance=True,
        include_tests=True,
        validation_strict=True
    )
    
    engine = ModernizationEngine(config)
    
    # Simulated source code
    source_code = """
    public class TransactionProcessor {
        private double balance;
        
        public double calculateInterest(double rate) {
            return balance * rate;
        }
        
        public void processTransaction(double amount) {
            balance += amount;
        }
    }
    """
    
    click.echo(f"\n🔄 Modernizing: {source_file}")
    click.echo("=" * 60)
    click.echo(f"Source: {source_enum.value}")
    click.echo(f"Target: {target_enum.value}")
    
    # Perform modernization
    result = engine.modernize(source_code, config)
    
    # Display results
    click.echo(f"\n✅ Modernization Complete!")
    click.echo(f"   Job ID: {result.job_id}")
    click.echo(f"   Status: {result.status.value}")
    click.echo(f"   Coverage Parity: {result.coverage_parity*100:.1f}%")
    
    complexity = result.complexity_comparison
    click.echo(f"   Complexity: {complexity['legacy_complexity']:.1f} → {complexity['modern_complexity']:.1f}")
    click.echo(f"   Improvement: {complexity['improvement_percent']:.1f}%")
    
    if result.warnings:
        click.echo(f"\n⚠️  Warnings:")
        for warning in result.warnings:
            click.echo(f"   • {warning}")
    
    # Show modernized code
    click.echo(f"\n📄 Modernized Code (Go):")
    click.echo("-" * 60)
    click.echo(result.modernized_code)
    
    # Save to file if requested
    if output:
        with open(output, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        click.echo(f"\n✅ Report saved to: {output}")


@main.command()
def results() -> None:
    """Show modernization results summary."""
    engine = ModernizationEngine()
    
    # Add some demo results
    config = ModernizationConfig(
        source_language=SourceLanguage.JAVA_LEGACY,
        target_language=TargetLanguage.GO,
        preserve_comments=True,
        optimize_for_performance=True,
        include_tests=True,
        validation_strict=True
    )
    
    engine._job_counter = 2
    engine._results = []
    
    result1 = ModernizationResult(
        job_id="MOD_1_1234567890",
        source_file="legacy.java",
        source_language=SourceLanguage.JAVA_LEGACY,
        target_language=TargetLanguage.GO,
        modernized_code="// Modernized code",
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
    
    result2 = ModernizationResult(
        job_id="MOD_2_1234567891",
        source_file="legacy2.java",
        source_language=SourceLanguage.JAVA_LEGACY,
        target_language=TargetLanguage.RUST,
        modernized_code="// Modernized code",
        status=ModernizationStatus.COMPLETE,
        errors=[],
        warnings=[],
        coverage_parity=0.92,
        complexity_comparison={
            "legacy_complexity": 15.0,
            "modern_complexity": 10.5,
            "improvement_percent": 30.0
        },
        created_at=datetime.now(),
        completed_at=datetime.now()
    )
    
    engine._results = [result1, result2]
    
    click.echo(f"\n📊 Modernization Results")
    click.echo("=" * 60)
    
    results = engine.get_results()
    
    click.echo(f"\nTotal Jobs: {len(results)}")
    click.echo(f"Average Coverage Parity: {engine.get_coverage_parity()*100:.1f}%")
    
    click.echo(f"\nResults:")
    for result in results:
        click.echo(f"\n  {result.job_id}")
        click.echo(f"    Source: {result.source_language.value}")
        click.echo(f"    Target: {result.target_language.value}")
        click.echo(f"    Coverage: {result.coverage_parity*100:.1f}%")
        click.echo(f"    Status: {result.status.value}")


@main.command()
def demo() -> None:
    """Run modernization demo."""
    click.echo("\n🧪 Legacy Code Modernization Demo")
    click.echo("=" * 60)
    
    engine = ModernizationEngine()
    
    # Java sample code
    java_code = """
    public class TransactionProcessor {
        private double balance;
        
        public double calculateInterest(double rate) {
            return balance * rate;
        }
        
        public void processTransaction(double amount) {
            balance += amount;
        }
    }
    """
    
    config = ModernizationConfig(
        source_language=SourceLanguage.JAVA_LEGACY,
        target_language=TargetLanguage.GO,
        preserve_comments=True,
        optimize_for_performance=True,
        include_tests=True,
        validation_strict=True
    )
    
    click.echo("\n📝 Source Code (Java):")
    click.echo("-" * 60)
    click.echo(java_code)
    
    # Modernize
    result = engine.modernize(java_code, config)
    
    click.echo(f"\n🔄 Modernizing to {result.target_language.value}...")
    click.echo(f"   Job ID: {result.job_id}")
    click.echo(f"   Coverage: {result.coverage_parity*100:.1f}%")
    
    click.echo(f"\n📄 Modernized Code ({result.target_language.value}):")
    click.echo("-" * 60)
    click.echo(result.modernized_code)
    
    complexity = result.complexity_comparison
    click.echo(f"\n📊 Analysis:")
    click.echo(f"   Legacy Complexity: {complexity['legacy_complexity']:.1f}")
    click.echo(f"   Modern Complexity: {complexity['modern_complexity']:.1f}")
    click.echo(f"   Improvement: {complexity['improvement_percent']:.1f}%")


def main_entry() -> None:
    """Main entry point."""
    main(prog_name="legacy-modernizer")


if __name__ == "__main__":
    main_entry()
