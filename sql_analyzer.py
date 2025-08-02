import sqlparse
import re
from typing import List, Dict, Any
from collections import defaultdict

class SQLAnalyzer:
    def __init__(self):
        self.performance_issues = {
            'missing_indexes': [],
            'inefficient_joins': [],
            'suboptimal_where_clauses': [],
            'unnecessary_columns': [],
            'missing_limits': [],
            'inefficient_aggregations': [],
            'cross_joins': [],
            'nested_subqueries': [],
            'wildcard_selects': [],
            'missing_partitioning': []
        }
    
    def parse_sql(self, sql_content: str) -> List[sqlparse.sql.Statement]:
        """Parse SQL content into individual statements"""
        try:
            statements = sqlparse.parse(sql_content)
            return [stmt for stmt in statements if stmt.get_type() != 'Comment']
        except Exception as e:
            raise Exception(f"Failed to parse SQL: {str(e)}")
    
    def analyze_queries(self, parsed_queries: List[sqlparse.sql.Statement]) -> List[Dict[str, Any]]:
        """Analyze each parsed query for performance issues"""
        results = []
        
        for query in parsed_queries:
            if not query.get_type() or query.get_type() == 'Comment':
                continue
                
            analysis = {
                'query_type': self._get_query_type(query),
                'tables': self._extract_tables(query),
                'columns': self._extract_columns(query),
                'joins': self._analyze_joins(query),
                'where_clause': self._analyze_where_clause(query),
                'group_by': self._analyze_group_by(query),
                'order_by': self._analyze_order_by(query),
                'limit': self._analyze_limit(query),
                'subqueries': self._find_subqueries(query),
                'issues': [],
                'complexity_score': 0,
                'estimated_performance': 'unknown'
            }
            
            # Detect issues
            analysis['issues'] = self._detect_issues(query, analysis)
            analysis['complexity_score'] = self._calculate_complexity_score(analysis)
            analysis['estimated_performance'] = self._estimate_performance(analysis)
            
            results.append(analysis)
        
        return results
    
    def _get_query_type(self, query) -> str:
        """Determine the type of SQL query"""
        tokens = [token.value.upper() for token in query.flatten()]
        
        if 'SELECT' in tokens:
            return 'SELECT'
        elif 'INSERT' in tokens:
            return 'INSERT'
        elif 'UPDATE' in tokens:
            return 'UPDATE'
        elif 'DELETE' in tokens:
            return 'DELETE'
        elif 'CREATE' in tokens:
            return 'CREATE'
        elif 'ALTER' in tokens:
            return 'ALTER'
        elif 'DROP' in tokens:
            return 'DROP'
        else:
            return 'UNKNOWN'
    
    def _extract_tables(self, query) -> List[str]:
        """Extract table names from the query"""
        tables = []
        from_seen = False
        
        for token in query.flatten():
            if token.value.upper() == 'FROM':
                from_seen = True
            elif from_seen and token.ttype is None and token.value.strip():
                if token.value.strip() not in ['AS', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'ON']:
                    tables.append(token.value.strip())
                if token.value.upper() in ['WHERE', 'GROUP', 'ORDER', 'HAVING', 'LIMIT']:
                    break
        
        return list(set(tables))
    
    def _extract_columns(self, query) -> List[str]:
        """Extract column names from SELECT clause"""
        columns = []
        select_seen = False
        from_seen = False
        
        for token in query.flatten():
            if token.value.upper() == 'SELECT':
                select_seen = True
            elif token.value.upper() == 'FROM':
                from_seen = True
                break
            elif select_seen and not from_seen:
                if token.ttype is None and token.value.strip() and token.value.strip() != ',':
                    columns.append(token.value.strip())
        
        return columns
    
    def _analyze_joins(self, query) -> Dict[str, Any]:
        """Analyze JOIN clauses for performance issues"""
        joins = {
            'join_count': 0,
            'join_types': [],
            'cross_joins': False,
            'missing_conditions': False
        }
        
        tokens = [token.value.upper() for token in query.flatten()]
        
        # Count joins
        joins['join_count'] = tokens.count('JOIN')
        
        # Check for cross joins
        if 'CROSS' in tokens:
            joins['cross_joins'] = True
        
        # Check join types
        for i, token in enumerate(tokens):
            if token in ['LEFT', 'RIGHT', 'INNER', 'OUTER', 'FULL']:
                if i + 1 < len(tokens) and tokens[i + 1] == 'JOIN':
                    joins['join_types'].append(f"{token} JOIN")
        
        return joins
    
    def _analyze_where_clause(self, query) -> Dict[str, Any]:
        """Analyze WHERE clause for optimization opportunities"""
        where_analysis = {
            'has_where': False,
            'conditions': [],
            'functions_used': [],
            'potential_issues': []
        }
        
        where_tokens = []
        in_where = False
        
        for token in query.flatten():
            if token.value.upper() == 'WHERE':
                in_where = True
                where_analysis['has_where'] = True
            elif in_where and token.value.upper() in ['GROUP', 'ORDER', 'HAVING', 'LIMIT']:
                break
            elif in_where:
                where_tokens.append(token.value)
        
        if where_analysis['has_where']:
            where_text = ' '.join(where_tokens)
            
            # Check for functions in WHERE clause
            function_patterns = [
                r'\b(UPPER|LOWER|TRIM|SUBSTRING|DATE|YEAR|MONTH|DAY)\s*\(',
                r'\b(ISNULL|COALESCE|NULLIF)\s*\(',
                r'\b(CONVERT|CAST)\s*\('
            ]
            
            for pattern in function_patterns:
                if re.search(pattern, where_text, re.IGNORECASE):
                    where_analysis['functions_used'].append(re.search(pattern, where_text, re.IGNORECASE).group(1))
            
            # Check for potential issues
            if 'LIKE' in where_text and '%' in where_text:
                where_analysis['potential_issues'].append('Wildcard at start of LIKE pattern')
            
            if 'OR' in where_text:
                where_analysis['potential_issues'].append('OR conditions may prevent index usage')
        
        return where_analysis
    
    def _analyze_group_by(self, query) -> Dict[str, Any]:
        """Analyze GROUP BY clause"""
        group_analysis = {
            'has_group_by': False,
            'columns': [],
            'with_aggregation': False
        }
        
        tokens = [token.value.upper() for token in query.flatten()]
        
        if 'GROUP BY' in ' '.join(tokens):
            group_analysis['has_group_by'] = True
            
            # Check for aggregation functions
            agg_functions = ['COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'GROUP_CONCAT']
            for func in agg_functions:
                if func in tokens:
                    group_analysis['with_aggregation'] = True
                    break
        
        return group_analysis
    
    def _analyze_order_by(self, query) -> Dict[str, Any]:
        """Analyze ORDER BY clause"""
        order_analysis = {
            'has_order_by': False,
            'columns': [],
            'has_limit': False
        }
        
        tokens = [token.value.upper() for token in query.flatten()]
        
        if 'ORDER BY' in ' '.join(tokens):
            order_analysis['has_order_by'] = True
        
        if 'LIMIT' in tokens:
            order_analysis['has_limit'] = True
        
        return order_analysis
    
    def _analyze_limit(self, query) -> Dict[str, Any]:
        """Analyze LIMIT clause"""
        limit_analysis = {
            'has_limit': False,
            'limit_value': None
        }
        
        tokens = [token.value for token in query.flatten()]
        
        for i, token in enumerate(tokens):
            if token.upper() == 'LIMIT' and i + 1 < len(tokens):
                try:
                    limit_analysis['limit_value'] = int(tokens[i + 1])
                    limit_analysis['has_limit'] = True
                except ValueError:
                    pass
                break
        
        return limit_analysis
    
    def _find_subqueries(self, query) -> List[Dict[str, Any]]:
        """Find and analyze subqueries"""
        subqueries = []
        
        def find_subqueries_recursive(token):
            if hasattr(token, 'tokens'):
                for subtoken in token.tokens:
                    if isinstance(subtoken, sqlparse.sql.Statement):
                        subqueries.append({
                            'type': 'subquery',
                            'content': str(subtoken)
                        })
                    find_subqueries_recursive(subtoken)
        
        find_subqueries_recursive(query)
        return subqueries
    
    def _detect_issues(self, query, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect performance issues in the query"""
        issues = []
        
        # Check for SELECT *
        if '*' in analysis['columns']:
            issues.append({
                'type': 'wildcard_select',
                'severity': 'medium',
                'message': 'SELECT * retrieves all columns, consider selecting only needed columns',
                'impact': 'Reduces network transfer and improves performance'
            })
        
        # Check for missing LIMIT
        if analysis['query_type'] == 'SELECT' and not analysis['limit']['has_limit']:
            issues.append({
                'type': 'missing_limit',
                'severity': 'low',
                'message': 'No LIMIT clause found, query may return large result sets',
                'impact': 'May cause memory issues and slow response times'
            })
        
        # Check for cross joins
        if analysis['joins']['cross_joins']:
            issues.append({
                'type': 'cross_join',
                'severity': 'high',
                'message': 'CROSS JOIN detected, this can cause performance issues',
                'impact': 'May result in Cartesian product with exponential growth'
            })
        
        # Check for functions in WHERE clause
        if analysis['where_clause']['functions_used']:
            issues.append({
                'type': 'functions_in_where',
                'severity': 'medium',
                'message': f"Functions used in WHERE clause: {', '.join(analysis['where_clause']['functions_used'])}",
                'impact': 'Functions in WHERE clause may prevent index usage'
            })
        
        # Check for multiple joins
        if analysis['joins']['join_count'] > 3:
            issues.append({
                'type': 'many_joins',
                'severity': 'medium',
                'message': f"Query has {analysis['joins']['join_count']} joins, consider query optimization",
                'impact': 'Multiple joins can significantly impact performance'
            })
        
        # Check for subqueries
        if analysis['subqueries']:
            issues.append({
                'type': 'subqueries',
                'severity': 'medium',
                'message': f"Query contains {len(analysis['subqueries'])} subquery(ies)",
                'impact': 'Subqueries may be less efficient than JOINs in some cases'
            })
        
        # Check for ORDER BY without LIMIT
        if analysis['order_by']['has_order_by'] and not analysis['limit']['has_limit']:
            issues.append({
                'type': 'order_without_limit',
                'severity': 'low',
                'message': 'ORDER BY without LIMIT may sort entire result set',
                'impact': 'Sorting large datasets can be expensive'
            })
        
        return issues
    
    def _calculate_complexity_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate a complexity score for the query"""
        score = 0
        
        # Base score
        score += 1
        
        # Add points for complexity factors
        score += len(analysis['tables']) * 2
        score += analysis['joins']['join_count'] * 3
        score += len(analysis['subqueries']) * 5
        score += len(analysis['where_clause']['functions_used']) * 2
        
        if analysis['group_by']['has_group_by']:
            score += 3
        
        if analysis['order_by']['has_order_by']:
            score += 2
        
        return score
    
    def _estimate_performance(self, analysis: Dict[str, Any]) -> str:
        """Estimate query performance based on analysis"""
        complexity_score = analysis['complexity_score']
        issues_count = len(analysis['issues'])
        
        if complexity_score <= 5 and issues_count == 0:
            return 'excellent'
        elif complexity_score <= 10 and issues_count <= 2:
            return 'good'
        elif complexity_score <= 15 and issues_count <= 4:
            return 'fair'
        else:
            return 'poor' 