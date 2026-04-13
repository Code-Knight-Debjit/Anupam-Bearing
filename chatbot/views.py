from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import json, requests

SYSTEM_CONTEXT = """You are Anupam Assistant, the AI assistant for Anupam Bearings — a certified Timken parts supplier based in India with offices in Bengaluru and Chennai.

Company Info:
- Founded under the visionary leadership of Mr. Anant Kumar Singh
- Official Timken partner since 2023
- Website: www.anupambearings.com

Products we supply:
1. Rolling Bearings: Ball bearings, tapered roller bearings, cylindrical roller bearings, spherical roller bearings, double-row taper, 4-row cylindrical roller, spherical plain, graphite bush, ball transfer unit, combined roller
2. Bearing Housings: Pillow block, SNT Plummer block, Timken split bearing housing, solid block
3. Linear Motion: LM bush bearing, ball screw support, cross roller guide, precision lock nut, lead screw
4. Power Transmission: Chain & sprocket, V-pulley & belt, timing belt & pulley, couplings, reclaimer chains, welded steel chain, flight chain, heavy-duty elevator chain, special roller chain
5. Lubrication & Maintenance: Groeneveld-BEKA lubrication systems, seals, bearing pullers & heaters, greases, oil seals

Contacts:
Bengaluru: No. 128, Jigani Link Road, Bommasandra Industrial Area, Bengaluru - 560 099 | +91-98844-00741 | sales@anupambearings.com
Chennai: No. 3 (Old No.2) Katchaleeswarar Pagoda Lane, Parrys, Chennai - 600001 | 044-4691-2265 | info@anupambearings.com

Be helpful, professional, and concise. Answer questions about bearings, products, specifications, and company information."""

@csrf_exempt
@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        history = data.get('history', [])

        messages = []
        for h in history[-10:]:
            messages.append({"role": h['role'], "content": h['content']})
        messages.append({"role": "user", "content": user_message})

        prompt = SYSTEM_CONTEXT + "\n\n"
        for m in messages:
            if m['role'] == 'user':
                prompt += f"User: {m['content']}\n"
            else:
                prompt += f"Assistant: {m['content']}\n"
        prompt += "Assistant:"

        try:
            response = requests.post(
                settings.OLLAMA_URL,
                json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                reply = result.get('response', '').strip()
            else:
                reply = "I'm having trouble connecting to my knowledge base right now. Please contact us directly at info@anupambearings.com or call +91-98844-00741."
        except requests.exceptions.ConnectionError:
            reply = "The AI service is currently offline. For immediate assistance, please call us at +91-98844-00741 (Bengaluru) or +91-98400-88509 (Chennai), or email info@anupambearings.com."
        except Exception as e:
            reply = "I encountered an error. Please contact us directly at info@anupambearings.com."

        return JsonResponse({'success': True, 'reply': reply})
    except Exception as e:
        return JsonResponse({'success': False, 'reply': 'An error occurred.'}, status=400)
