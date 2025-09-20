from decimal import Decimal
from datetime import date, timedelta
from django.db.models import Sum
from django.conf import settings
from .models import Expense
import google.generativeai as genai

def get_expense_summary_for_gemini(user):
    """Get expense summary for the current and previous month"""
    today = date.today()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)
    
    # Get total expenses for this month
    total_this_month = Expense.objects.filter(
        user=user, 
        date__gte=first_day_this_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Get total expenses for last month
    total_last_month = Expense.objects.filter(
        user=user, 
        date__gte=first_day_last_month, 
        date__lte=last_day_last_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Calculate percentage change
    if total_last_month and total_last_month != Decimal('0.00'):
        pct_change = (total_this_month - total_last_month) / total_last_month * Decimal(100)
    else:
        pct_change = None
    
    # Get top categories for this month
    categories = list(
        Expense.objects.filter(user=user, date__gte=first_day_this_month)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    
    top_categories = []
    for cat in categories:
        cat_total = cat.get('total') or Decimal('0.00')
        category_name = cat.get('category') or 'Uncategorized'
        pct = (cat_total / total_this_month * Decimal(100)) if total_this_month != Decimal('0.00') else Decimal('0.00')
        top_categories.append({
            'category': category_name,
            'total': float(cat_total),
            'percentage': float(round(pct, 2))
        })
    
    summary = {
        'total_this_month': float(total_this_month),
        'total_last_month': float(total_last_month),
        'percentage_change': float(round(pct_change, 2)) if pct_change is not None else None,
        'top_categories': top_categories[:5]  # Top 5 categories
    }
    
    return summary

def build_prompt(summary):
    """Build a simple, safe prompt for Gemini"""
    total_this = summary['total_this_month']
    total_last = summary['total_last_month']
    
    # Simple, clean prompt with Naira context
    prompt = f"""I am a personal finance assistant. Please analyze this spending data in Nigerian Naira:

This month total: ₦{total_this:.2f}
Last month total: ₦{total_last:.2f}

"""
    
    if summary['percentage_change'] is not None:
        change = summary['percentage_change']
        if change > 0:
            prompt += f"Spending increased by {change:.1f}%\n"
        else:
            prompt += f"Spending decreased by {abs(change):.1f}%\n"
    
    if summary['top_categories']:
        prompt += "\nTop categories:\n"
        for i, cat in enumerate(summary['top_categories'][:3], 1):
            prompt += f"{i}. {cat['category']}: ₦{cat['total']:.2f}\n"
    
    prompt += "\nProvide 3 brief financial insights as bullet points using Nigerian Naira context."
    
    return prompt

def generate_insights(user):
    """Generate spending insights using Gemini AI"""
    try:
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Get expense summary
        summary = get_expense_summary_for_gemini(user)
        
        # If no expenses, return a simple message
        if summary['total_this_month'] == 0:
            return ["No expenses recorded this month - great job saving money!", 
                   "Consider setting up a budget to track your financial goals in Naira.", 
                   "Start tracking expenses to get personalized insights for Nigerian spending patterns."]
        
        # Build prompt
        prompt = build_prompt(summary)
        
        # Generate content with Gemini - try with minimal settings first
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # First try with very basic settings
        try:
            response = model.generate_content(prompt)
            
            # Check if we have a valid response
            if response.parts and response.text:
                insights_text = response.text
            else:
                # If blocked, try a super simple fallback prompt
                fallback_prompt = f"Give 3 tips for managing money when spending ₦{summary['total_this_month']:.0f} per month in Nigeria."
                response = model.generate_content(fallback_prompt)
                insights_text = response.text if response.text else "Unable to generate insights"
                
        except Exception as api_error:
            print(f"API Error: {api_error}")
            # Use fallback prompt as last resort
            fallback_prompt = "Give 3 general money saving tips for Nigeria."
            try:
                response = model.generate_content(fallback_prompt)
                insights_text = response.text if response.text else "Basic financial tips needed"
            except:
                insights_text = "• Track your expenses daily in Naira\n• Set a monthly budget in Nigerian Naira\n• Review spending weekly for better financial planning"
        insights = []
        
        # Simple parsing - split by lines and clean up
        lines = insights_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                # Remove bullet point markers
                insight = line.lstrip('•-* ').strip()
                if insight:
                    insights.append(insight)
        
        # Ensure we have exactly 3 insights
        if len(insights) < 3:
            insights.extend([
                "Keep tracking your expenses to identify spending patterns.",
                "Consider reviewing your largest expense categories for potential savings.",
                "Regular expense tracking helps with better financial planning."
            ])
        
        return insights[:3]  # Return only first 3
        
    except Exception as e:
        # Fallback insights if API fails
        print(f"Error generating insights: {e}")
        return [
            "Unable to generate AI insights at the moment.",
            "Please review your spending categories manually.",
            "Consider setting a monthly budget to track your progress."
        ]