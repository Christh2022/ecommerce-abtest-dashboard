// Reconnaissance vocale uniquement (sans synthèse vocale)
console.log('🎙️ Script welcome_speech.js chargé');

window.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOMContentLoaded - Page:', window.location.pathname);
    
    // Vérifier si on est sur la landing page
    if (window.location.pathname === '/') {
        console.log('✅ Sur la landing page - Initialisation de la reconnaissance vocale');
        
        // Créer un bouton pour activer l'audio (requis par les navigateurs modernes)
        const activateButton = document.createElement('button');
        activateButton.innerHTML = '🎤 Activer la Reconnaissance Vocale';
        activateButton.style.cssText = 'position: fixed; bottom: 80px; right: 30px; z-index: 10000; padding: 15px 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 50px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5); animation: pulse 2s infinite;';
        document.body.appendChild(activateButton);
        console.log('✅ Bouton d\'activation créé');
        
        // Attendre que la page soit complètement chargée
        setTimeout(function() {
            console.log('⏰ Initialisation de la reconnaissance vocale');
            
            // Initialiser la reconnaissance vocale
            let recognition = null;
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.lang = 'fr-FR';
                recognition.continuous = true;
                recognition.interimResults = true;
                
                recognition.onstart = function() {
                    console.log('🎤 En écoute... Parlez maintenant');
                    console.log('🎤 Langue détection:', recognition.lang);
                    console.log('🎤 Continuous:', recognition.continuous);
                    console.log('🎤 InterimResults:', recognition.interimResults);
                };
                
                recognition.onspeechstart = function() {
                    console.log('🗣️ Parole détectée - traitement en cours...');
                };
                
                recognition.onspeechend = function() {
                    console.log('🛑 Fin de la parole détectée');
                };
                
                recognition.onaudiostart = function() {
                    console.log('🎙️ Audio capté par le microphone');
                };
                
                recognition.onaudioend = function() {
                    console.log('🎙️ Fin de capture audio');
                };
                
                recognition.onsoundstart = function() {
                    console.log('🔊 Son détecté');
                };
                
                recognition.onsoundend = function() {
                    console.log('🔇 Fin du son');
                };
                
                recognition.onresult = function(event) {
                    console.log('✅ RÉSULTAT REÇU !');
                    console.log('📦 Event complet:', event);
                    console.log('📦 Nombre de résultats:', event.results.length);
                    
                    // Gérer les résultats intermédiaires et finaux
                    const lastResultIndex = event.results.length - 1;
                    const result = event.results[lastResultIndex];
                    const transcript = result[0].transcript.toLowerCase();
                    const isFinal = result.isFinal;
                    
                    console.log('📝 Transcript:', transcript, isFinal ? '(FINAL)' : '(intermédiaire)');
                    console.log('📝 Longueur:', transcript.length, 'caractères');
                    console.log('📝 Confiance:', result[0].confidence);
                    
                    // Ne traiter que les résultats finaux
                    if (!isFinal) {
                        console.log('⏳ En attente du résultat final...');
                        return;
                    }
                    
                    // Traiter la commande
                    let responseText = '';
                    
                    // Détecter les demandes d'explication de l'accueil
                    const isExplainRequest = transcript.includes('explique') || 
                                            transcript.includes('expliquer') || 
                                            transcript.includes('explique-moi') ||
                                            transcript.includes('peux tu') ||
                                            transcript.includes('peux-tu') ||
                                            transcript.includes('tu peux') ||
                                            transcript.includes('présente') ||
                                            transcript.includes('présenter');
                    
                    const isAboutHome = transcript.includes('accueil') || 
                                       transcript.includes('page') || 
                                       transcript.includes('application') ||
                                       transcript.includes('plateforme') ||
                                       transcript.includes('site');
                    
                    if (isExplainRequest && isAboutHome) {
                        console.log('✅ Commande détectée: Explication de l\'accueil');
                        responseText = 'Bienvenue sur notre plateforme d\'analyse A/B Testing. Cette application vous permet de visualiser et analyser les résultats de tests A/B pour optimiser vos décisions marketing. Vous pouvez accéder au dashboard principal, consulter les visualisations interactives, ou calculer la significativité statistique de vos tests.';
                    }
                    else if (transcript.includes('dashboard') || transcript.includes('tableau de bord')) {
                        responseText = 'Navigation vers le dashboard...';
                        setTimeout(() => { window.location.href = '/dashboard'; }, 1500);
                    }
                    else if (transcript.includes('visualisation') || transcript.includes('graphique')) {
                        responseText = 'Navigation vers les visualisations...';
                        setTimeout(() => { window.location.href = '/visualizations'; }, 1500);
                    }
                    else if (transcript.includes('calculateur') || transcript.includes('calcul')) {
                        responseText = 'Navigation vers le calculateur A/B...';
                        setTimeout(() => { window.location.href = '/calculator'; }, 1500);
                    }
                    else if (transcript.includes('simulation')) {
                        responseText = 'Navigation vers les simulations...';
                        setTimeout(() => { window.location.href = '/simulations'; }, 1500);
                    }
                    else if (transcript.includes('résultat') || transcript.includes('résultats')) {
                        responseText = 'Navigation vers les résultats...';
                        setTimeout(() => { window.location.href = '/results'; }, 1500);
                    }
                    else if (transcript.includes('connexion') || transcript.includes('connecter')) {
                        responseText = 'Redirection vers la page de connexion...';
                        setTimeout(() => { window.location.href = '/login'; }, 1500);
                    }
                    else {
                        console.log('⚠️ Commande non reconnue');
                        responseText = 'Commande entendue: "' + transcript + '". Commandes disponibles: explique l\'accueil, va sur le dashboard, visualisations, calculateur, simulations, résultats, connexion.';
                    }
                    
                    console.log('💬 Réponse:', responseText);
                    
                    // Recommencer l'écoute après 2 secondes
                    setTimeout(function() {
                        if (recognition) {
                            console.log('🔄 Relance de l\'écoute...');
                            try {
                                recognition.start();
                            } catch(e) {
                                console.warn('⚠️ Reconnaissance déjà active');
                            }
                        }
                    }, 2000);
                    
                    // Stocker la commande
                    sessionStorage.setItem('userCommand', transcript);
                };
                
                recognition.onerror = function(event) {
                    console.error('❌ Erreur de reconnaissance vocale:', event.error);
                    console.error('❌ Détails erreur:', event);
                    
                    if (event.error === 'not-allowed') {
                        const errorMsg = 'Permission microphone refusée. Veuillez autoriser l\'accès au microphone dans les paramètres de votre navigateur.';
                        console.error('🚫', errorMsg);
                    }
                    else if (event.error === 'no-speech') {
                        console.warn('⚠️ Aucune parole détectée. Réessayez.');
                    }
                    else if (event.error === 'audio-capture') {
                        console.error('❌ Erreur de capture audio. Vérifiez votre microphone.');
                    }
                    else if (event.error === 'network') {
                        console.error('❌ Erreur réseau. Vérifiez votre connexion internet.');
                    }
                };
                
                recognition.onend = function() {
                    console.log('🛑 Reconnaissance vocale terminée');
                    console.log('💡 Pour réactiver, cliquez à nouveau sur le bouton');
                };
                
                recognition.onnomatch = function() {
                    console.warn('⚠️ Aucun résultat reconnu - Réessayez en parlant plus clairement');
                };
                
                // Fonction pour démarrer la reconnaissance
                function startRecognition() {
                    console.log('👂 Démarrage de la reconnaissance vocale...');
                    
                    if (recognition) {
                        // Test si le micro capture vraiment
                        navigator.mediaDevices.getUserMedia({ audio: true })
                            .then(function(testStream) {
                                console.log('🎤 Test micro - Stream obtenu:', testStream);
                                console.log('🎤 Pistes audio:', testStream.getAudioTracks());
                                
                                const audioTrack = testStream.getAudioTracks()[0];
                                if (audioTrack) {
                                    console.log('🎤 Piste audio active:', audioTrack.enabled);
                                    console.log('🎤 État piste:', audioTrack.readyState);
                                    console.log('🎤 Label:', audioTrack.label);
                                }
                                
                                // Arrêter le stream de test
                                testStream.getTracks().forEach(track => track.stop());
                                
                                // Maintenant lancer la reconnaissance
                                console.log('🔍 État recognition avant start:', recognition);
                                try {
                                    recognition.start();
                                    console.log('✅ recognition.start() appelé avec succès');
                                    console.log('⏰ Timeout de sécurité: 10 secondes');
                                    
                                    // Timeout de sécurité - arrêter après 10 secondes si rien ne se passe
                                    let recognitionTimeout = setTimeout(function() {
                                        console.log('⏱️ Timeout atteint - rien capté en 10 secondes');
                                        console.log('⏱️ Arrêt de la reconnaissance...');
                                        try {
                                            recognition.stop();
                                        } catch(e) {
                                            console.error('⏱️ Erreur lors de l\'arrêt:', e);
                                        }
                                    }, 10000);
                                    
                                    // Annuler le timeout si onstart se déclenche
                                    const originalOnStart = recognition.onstart;
                                    recognition.onstart = function() {
                                        console.log('🎤 onstart déclenché - annulation du timeout');
                                        clearTimeout(recognitionTimeout);
                                        if (originalOnStart) originalOnStart.apply(this, arguments);
                                    };
                                    
                                } catch(e) {
                                    console.error('❌ Erreur démarrage reconnaissance:', e);
                                    console.error('❌ Type erreur:', e.name);
                                    console.error('❌ Message:', e.message);
                                }
                            })
                            .catch(function(err) {
                                console.error('❌ Erreur test micro:', err);
                                console.error('❌ Le microphone ne répond pas');
                            });
                    }
                }
                
                // Fonction pour activer l'assistant vocal
                function startVoiceAssistant() {
                    console.log('🎬 Activation de la reconnaissance vocale par l\'utilisateur');
                    
                    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                        console.log('📱 Demande de permission microphone...');
                        navigator.mediaDevices.getUserMedia({ audio: true })
                            .then(function(stream) {
                                console.log('✅ Permission microphone accordée');
                                // Arrêter le stream immédiatement (on n'en a pas besoin, c'était juste pour la permission)
                                stream.getTracks().forEach(track => track.stop());
                                
                                activateButton.remove();
                                proceedWithVoiceAssistant();
                            })
                            .catch(function(err) {
                                console.error('❌ Permission microphone refusée:', err);
                                alert('🎤 Permission microphone requise\n\n' + 
                                      'Pour utiliser la reconnaissance vocale, vous devez autoriser l\'accès au microphone.\n\n' +
                                      'Veuillez:\n' +
                                      '1. Autoriser le microphone quand le navigateur le demande\n' +
                                      '2. Ou cliquer sur l\'icône 🔒 dans la barre d\'adresse\n' +
                                      '3. Puis réessayer');
                            });
                    } else {
                        console.warn('⚠️ getUserMedia non supporté, on essaie quand même...');
                        activateButton.remove();
                        proceedWithVoiceAssistant();
                    }
                }
                
                // Fonction pour continuer avec la reconnaissance vocale
                function proceedWithVoiceAssistant() {
                    console.log('🎙️ Lancement de la reconnaissance vocale...');
                    startRecognition();
                }
                
                // Ajouter l'événement au bouton
                activateButton.addEventListener('click', startVoiceAssistant);
                console.log('🎤 Reconnaissance vocale prête - Cliquez sur le bouton pour activer (permission microphone sera demandée)');
            } else {
                console.warn('⚠️ La reconnaissance vocale n\'est pas supportée par ce navigateur');
            }
        }, 1000);
    }
});
