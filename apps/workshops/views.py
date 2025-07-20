from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.http import JsonResponse
from .models import Workshop, Enrollment


class WorkshopListView(ListView):
    model = Workshop
    template_name = 'workshops/list.html'
    context_object_name = 'workshops'
    paginate_by = 12
    
    def get_queryset(self):
        return Workshop.objects.filter(is_active=True).select_related('category', 'level')


class WorkshopDetailView(DetailView):
    model = Workshop
    template_name = 'workshops/detail.html'
    context_object_name = 'workshop'
    
    def get_queryset(self):
        return Workshop.objects.filter(is_active=True).select_related('category', 'level')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context['user_enrolled'] = Enrollment.objects.filter(
                user=self.request.user,
                workshop=self.object,
                status='enrolled'
            ).exists()
        else:
            context['user_enrolled'] = False
            
        return context


class EnrollView(LoginRequiredMixin, View):
    def post(self, request, slug):
        workshop = get_object_or_404(Workshop, slug=slug, is_active=True)
        
        # Check if user is already enrolled
        existing_enrollment = Enrollment.objects.filter(
            user=request.user,
            workshop=workshop
        ).first()
        
        if existing_enrollment:
            if existing_enrollment.status == 'enrolled':
                messages.warning(request, 'Você já está inscrito neste workshop.')
            else:
                # Reactivate enrollment
                existing_enrollment.status = 'enrolled'
                existing_enrollment.save()
                messages.success(request, f'Inscrição reativada no workshop "{workshop.title}"!')
        else:
            # Check if workshop is full
            if workshop.is_full:
                messages.error(request, 'Este workshop está lotado.')
            elif not workshop.is_registration_open:
                messages.error(request, 'As inscrições para este workshop já foram encerradas.')
            else:
                # Create new enrollment
                Enrollment.objects.create(
                    user=request.user,
                    workshop=workshop
                )
                messages.success(request, f'Inscrição realizada com sucesso no workshop "{workshop.title}"!')
        
        if request.headers.get('HX-Request'):
            # HTMX request
            return JsonResponse({'success': True})
        
        return redirect('workshops:detail', slug=workshop.slug)


class CancelEnrollmentView(LoginRequiredMixin, View):
    def post(self, request, slug):
        workshop = get_object_or_404(Workshop, slug=slug)
        
        enrollment = get_object_or_404(
            Enrollment,
            user=request.user,
            workshop=workshop,
            status='enrolled'
        )
        
        enrollment.status = 'cancelled'
        enrollment.save()
        
        messages.success(request, f'Inscrição cancelada no workshop "{workshop.title}".')
        
        if request.headers.get('HX-Request'):
            return JsonResponse({'success': True})
        
        return redirect('workshops:detail', slug=workshop.slug)